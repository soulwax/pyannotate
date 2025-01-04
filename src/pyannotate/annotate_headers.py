# File: src/pyannotate/annotate_headers.py
"""Core functionality for adding and updating file headers."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Set, List, Tuple


@dataclass
class FilePattern:
    """Configuration for file patterns and their comment styles."""

    extensions: List[str]
    comment_start: str
    comment_end: str = ""  # Empty string for single-line comment styles


# Define supported file patterns and their comment styles
PATTERNS = [
    FilePattern([".py", ".sh", ".bash"], "#", ""),
    FilePattern([".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".h", ".hpp"], "//", ""),
    FilePattern([".html", ".xml", ".svg"], "<!--", "-->"),
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

# Define special config files and their comment styles as (start, end) tuples
CONFIG_FILES: dict[str, Tuple[str, str]] = {
    ".gitignore": ("#", ""),
    ".dockerignore": ("#", ""),
    ".env": ("#", ""),
}


def _normalize_path(path: str) -> str:
    """Normalize path separators to forward slashes."""
    return path.replace(os.sep, "/")


def _create_header(file_path: Path, project_root: Path) -> str:
    """Create the header content for a file."""
    relative_path = os.path.relpath(file_path, project_root)
    return f"File: {_normalize_path(relative_path)}"


def _get_comment_style(file_path: Path) -> Optional[Tuple[str, str]]:
    """Determine the appropriate comment style for a given file."""
    # Check if it's a special config file
    if file_path.name in CONFIG_FILES:
        return CONFIG_FILES[file_path.name]

    # Check file extension patterns
    for pattern in PATTERNS:
        if any(str(file_path).lower().endswith(ext) for ext in pattern.extensions):
            return (pattern.comment_start, pattern.comment_end)
    return None


def _is_html_like(file_path: Path) -> bool:
    """Check if the file is HTML-like and needs special handling."""
    return any(str(file_path).lower().endswith(ext) for ext in [".html", ".xml", ".svg"])


def _create_header_line(comment_start: str, comment_end: str, header: str) -> str:
    """Create a properly formatted header line with comments."""
    if comment_end:
        return f"{comment_start} {header} {comment_end}"
    return f"{comment_start} {header}"


def process_file(file_path: Path, project_root: Path) -> None:
    """Process a single file, adding or updating its header."""
    if not file_path.is_file():
        logging.warning("File not found: %s", file_path)
        return

    comment_style = _get_comment_style(file_path)
    if not comment_style:
        return

    comment_start, comment_end = comment_style

    try:
        content = file_path.read_text()
        header = _create_header(file_path, project_root)
        header_line = _create_header_line(comment_start, comment_end, header)

        # Split content into lines
        lines = content.splitlines()

        # Handle empty files
        if not lines:
            new_content = f"{header_line}\n"
            file_path.write_text(new_content)
            return

        # Handle files with shebang
        if lines[0].startswith("#!"):
            shebang = lines[0]
            remaining_lines = lines[1:]

            # Remove existing header if present
            if remaining_lines and any(
                line.strip().startswith(f"{comment_start} File:") for line in remaining_lines[:1]
            ):
                remaining_lines = remaining_lines[1:]

            new_content = f"{shebang}\n{header_line}\n" + "\n".join(remaining_lines)

        # Handle HTML-like files
        elif _is_html_like(file_path):
            # Keep XML/DOCTYPE declaration as first line if present
            if lines[0].lower().startswith(("<!doctype", "<?xml")):
                first_line = lines[0]
                rest_lines = lines[1:]

                # Remove existing header if present
                if rest_lines and any(
                    line.strip().startswith(f"{comment_start} File:") for line in rest_lines[:1]
                ):
                    rest_lines = rest_lines[1:]

                new_content = f"{first_line}\n{header_line}\n" + "\n".join(rest_lines)
            else:
                # Remove existing header if present
                if any(line.strip().startswith(f"{comment_start} File:") for line in lines[:1]):
                    lines = lines[1:]
                new_content = f"{header_line}\n" + "\n".join(lines)

        # Handle all other files
        else:
            # Remove existing header if present
            if any(line.strip().startswith(f"{comment_start} File:") for line in lines[:1]):
                lines = lines[1:]
            new_content = f"{header_line}\n" + "\n".join(lines)

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
