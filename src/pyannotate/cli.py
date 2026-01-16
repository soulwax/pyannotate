# File: src/pyannotate/cli.py

"""CLI interface for PyAnnotate."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from .annotate_headers import walk_directory
from .backup import revert_files, save_backup
from .config import load_config


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
        help="Revert files to their state before the last pyannotate run",
    )
    return parser.parse_args(args)


def _handle_revert(project_root: Path, dry_run: bool) -> int:
    """Handle revert mode."""
    if dry_run:
        logging.info("DRY-RUN MODE: Previewing revert operation")
    else:
        logging.info("Reverting files to state before last pyannotate run")
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


def _handle_annotation(project_root: Path, dry_run: bool, config) -> int:
    """Handle normal annotation mode."""
    if dry_run:
        logging.info("DRY-RUN MODE: No files will be modified")
        logging.info("Starting file annotation preview from: %s", project_root)
    else:
        logging.info("Starting file annotation from: %s", project_root)

    backup_content: dict = {}
    stats = walk_directory(
        project_root,
        project_root,
        dry_run=dry_run,
        config=config,
        backup_content=backup_content,
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

        if args.revert:
            return _handle_revert(project_root, args.dry_run)

        return _handle_annotation(project_root, args.dry_run, config)

    except (OSError, AnnotationError) as e:
        logging.error("An error occurred: %s", e)
        if args.verbose:
            logging.exception("Detailed error information:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
