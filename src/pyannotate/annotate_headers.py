# File: src/pyannotate/annotate_headers.py
"""Core functionality for adding and updating file headers."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Set, List


@dataclass
class FilePattern:
    """Configuration for file patterns and their comment styles."""

    extensions: List[str]  # Use List from typing
    comment_style: str


# Define supported file patterns and their comment styles
PATTERNS = [
    FilePattern([".py", ".sh", ".bash"], "#"),
    FilePattern([".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".h", ".hpp"], "//"),
    FilePattern([".html", ".xml", ".svg"], "<!--"),
]

# Define directories to ignore
IGNORED_DIRS: Set[str] = {
    "__pycache__",
    "node_modules",
    ".git",
    ".hg",
    ".svn",
    "venv",
    ".venv",
}

# Define special config files and their comment styles
CONFIG_FILES = {
    ".gitignore": "#",
    ".dockerignore": "#",
    ".env": "#",
}


def _normalize_path(path: str) -> str:
    """Normalize path separators to forward slashes."""
    return path.replace(os.sep, "/")


def _create_header(file_path: Path, project_root: Path) -> str:
    """Create the header content for a file."""
    relative_path = os.path.relpath(file_path, project_root)
    return f"File: {_normalize_path(relative_path)}"


def _get_comment_style(file_path: Path) -> Optional[str]:
    """Determine the appropriate comment style for a given file."""
    # Check if it's a special config file
    if file_path.name in CONFIG_FILES:
        return CONFIG_FILES[file_path.name]

    # Check file extension patterns
    for pattern in PATTERNS:
        if any(str(file_path).lower().endswith(ext) for ext in pattern.extensions):
            return pattern.comment_style
    return None


def process_file(file_path: Path, project_root: Path) -> None:
    """Process a single file, adding or updating its header."""
    if not file_path.is_file():
        logging.warning("File not found: %s", file_path)
        return

    comment_style = _get_comment_style(file_path)
    if not comment_style:
        return

    try:
        content = file_path.read_text()
        header = _create_header(file_path, project_root)
        header_line = f"{comment_style} {header}"

        # Split content into lines
        lines = content.splitlines()
        if not lines:
            new_content = f"{header_line}\n"
        elif lines[0].startswith("#!"):
            # Preserve shebang line for shell scripts
            shebang = lines[0]
            remaining_content = "\n".join(lines[1:]).lstrip()

            # Check if header already exists and remove it
            remaining_lines = remaining_content.splitlines()
            if remaining_lines and remaining_lines[0].startswith(f"{comment_style} File:"):
                remaining_content = "\n".join(remaining_lines[1:]).lstrip()

            new_content = f"{shebang}\n{header_line}\n{remaining_content}"
        else:
            # Remove existing header if present
            if lines[0].startswith(f"{comment_style} File:"):
                content = "\n".join(lines[1:]).lstrip()
            new_content = f"{header_line}\n{content}"

        file_path.write_text(new_content)
        logging.info("Updated header in: %s", file_path)
    except OSError as e:
        logging.error("Failed to process %s: %s", file_path, e)


def walk_directory(directory: Path, project_root: Path) -> None:
    """Walk through directory and process files recursively."""
    try:
        for item in directory.iterdir():
            if item.is_dir():
                if item.name not in IGNORED_DIRS:
                    walk_directory(item, project_root)
            else:
                process_file(item, project_root)
    except OSError as e:
        logging.error("Error accessing directory %s: %s", directory, e)
