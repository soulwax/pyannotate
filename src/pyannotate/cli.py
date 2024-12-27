"""CLI interface for PyAnnotate."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from .annotate_headers import walk_directory


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


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


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

        logging.info("Starting file annotation from: %s", project_root)
        walk_directory(project_root, project_root)
        logging.info("File annotation complete!")
        return 0

    except (OSError, AnnotationError) as e:
        logging.error("An error occurred: %s", e)
        if args.verbose:
            logging.exception("Detailed error information:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
