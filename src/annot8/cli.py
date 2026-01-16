# File: src/annot8/cli.py
# pylint: disable=duplicate-code

"""CLI interface for Annot8."""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from .annotate_headers import walk_directory
from .backup import revert_files, save_backup
from .config import load_config
from .git_integration import get_git_root, is_git_repository


class AnnotationError(Exception):
    """Base exception for annotation errors."""


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def parse_args(args=None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Add or update file headers in your project files."
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    parser.add_argument(
        "--revert",
        action="store_true",
        help="Revert files to their state before the last annot8 run",
    )
    parser.add_argument(
        "--git",
        action="store_true",
        help="Process only files tracked by git",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Process only files staged for commit",
    )
    parser.add_argument(
        "--use-git-metadata",
        action="store_true",
        help="Use git metadata (author, email, dates) for headers",
    )
    parser.add_argument(
        "--install-hook",
        action="store_true",
        help="Install pre-commit hook to annotate staged files",
    )
    return parser.parse_args(args)


def _handle_revert(project_root: Path, dry_run: bool) -> int:
    """Handle revert mode."""
    if dry_run:
        logging.info("DRY-RUN MODE: Previewing revert operation")
    else:
        logging.info("Reverting files to state before last annot8 run")
    stats = revert_files(project_root, dry_run=dry_run)
    if dry_run:
        logging.info("=" * 60)
        logging.info("DRY-RUN REVERT SUMMARY:")
        logging.info("  Files that would be reverted: %d", stats["reverted"])
        logging.info("  Files that no longer exist: %d", stats["missing"])
        logging.info("  Errors: %d", stats["errors"])
        logging.info("=" * 60)
        logging.info("Run without --dry-run to apply revert")
    else:
        logging.info("Revert complete!")
        logging.info("  Files reverted: %d", stats["reverted"])
        logging.info("  Files missing: %d", stats["missing"])
        logging.info("  Errors: %d", stats["errors"])
    return 0


def _install_pre_commit_hook(project_root: Path) -> int:
    """Install pre-commit hook to annotate staged files."""
    if not is_git_repository(project_root):
        logging.error("Not a git repository. Cannot install pre-commit hook.")
        return 1

    git_root = get_git_root(project_root)
    if not git_root:
        logging.error("Could not determine git root directory")
        return 1

    hooks_dir = git_root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_path = hooks_dir / "pre-commit"
    hook_content = """#!/bin/sh
# Pre-commit hook installed by annot8
# Annotates staged files with headers

annot8 --staged --use-git-metadata
"""
    try:
        hook_path.write_text(hook_content, encoding="utf-8")
        # Make executable on Unix-like systems
        os.chmod(hook_path, 0o755)
        logging.info("Pre-commit hook installed at %s", hook_path)
        logging.info("Staged files will be automatically annotated on commit")
        return 0
    except OSError as e:
        logging.error("Failed to install pre-commit hook: %s", e)
        return 1


def _handle_annotation(
    project_root: Path, dry_run: bool, config, git_mode: Optional[str], use_git_metadata: bool
) -> int:
    """Handle normal annotation mode."""
    if dry_run:
        logging.info("DRY-RUN MODE: No files will be modified")
        logging.info("Starting file annotation preview from: %s", project_root)
    else:
        logging.info("Starting file annotation from: %s", project_root)

    if git_mode:
        if not is_git_repository(project_root):
            logging.error("Not a git repository. Cannot use --git or --staged flags.")
            return 1
        if git_mode == "tracked":
            logging.info("Processing only git-tracked files")
        elif git_mode == "staged":
            logging.info("Processing only staged files")

    if use_git_metadata:
        if not is_git_repository(project_root):
            logging.warning("Not a git repository. Git metadata will not be available.")
        else:
            logging.info("Using git metadata for headers")

    backup_content: dict = {}
    stats = walk_directory(
        project_root,
        project_root,
        dry_run=dry_run,
        config=config,
        backup_content=backup_content,
        git_mode=git_mode,
        use_git_metadata=use_git_metadata,
    )

    if not dry_run and backup_content:
        save_backup(project_root, backup_content)
        logging.debug("Backup saved for %d files", len(backup_content))

    if dry_run:
        logging.info("=" * 60)
        logging.info("DRY-RUN SUMMARY:")
        logging.info("  Files that would be modified: %d", stats["modified"])
        logging.info("  Files that would be skipped: %d", stats["skipped"])
        logging.info("  Files already up to date: %d", stats["unchanged"])
        logging.info("=" * 60)
        logging.info("Run without --dry-run to apply these changes")
    else:
        logging.info("File annotation complete!")
        logging.info("  Files modified: %d", stats["modified"])
        logging.info("  Files skipped: %d", stats["skipped"])
        logging.info("  Files unchanged: %d", stats["unchanged"])
    return 0


def main(directory: Optional[Path] = None) -> int:
    """Main entry point for the CLI."""
    args = parse_args()
    if directory:
        args.directory = directory
    setup_logging(args.verbose)

    try:
        project_root = args.directory.resolve()
        if not project_root.is_dir():
            logging.error("Directory not found: %s", project_root)
            return 1

        config = load_config(project_root)

        if args.install_hook:
            return _install_pre_commit_hook(project_root)

        if args.revert:
            return _handle_revert(project_root, args.dry_run)

        # Determine git mode
        git_mode = None
        if args.staged:
            git_mode = "staged"
        elif args.git:
            git_mode = "tracked"

        return _handle_annotation(
            project_root, args.dry_run, config, git_mode, args.use_git_metadata
        )

    except (OSError, AnnotationError) as e:
        logging.error("An error occurred: %s", e)
        if args.verbose:
            logging.exception("Detailed error information:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
