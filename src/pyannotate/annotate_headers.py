# File: src/pyannotate/annotate_headers.py
"""Core functionality for adding and updating file headers."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Set, List, Tuple, Dict


@dataclass
class FilePattern:
    """Configuration for file patterns and their comment styles."""

    extensions: List[str]
    comment_start: str
    comment_end: str = ""  # Empty string for single-line comment styles


# Define supported file patterns and their comment styles
PATTERNS = [
    FilePattern([".py", ".sh", ".bash", ".ps1"], "#", ""),
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
CONFIG_FILES: Dict[str, Tuple[str, str]] = {
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


def _has_existing_header(lines: List[str], comment_start: str, start_index: int = 0) -> bool:
    """Check if file has an existing header at the specified start index."""
    return bool(lines[start_index:]) and any(
        line.strip().startswith(f"{comment_start} File:")
        for line in lines[start_index : start_index + 1]
    )


def _remove_existing_header(
    lines: List[str], comment_start: str, start_index: int = 0
) -> List[str]:
    """Remove existing header if present, starting from the specified index."""
    if _has_existing_header(lines, comment_start, start_index):
        return lines[:start_index] + lines[start_index + 1 :]
    return lines


def _process_empty_file(header_line: str) -> str:
    """Process an empty file."""
    return f"{header_line}\n"


def _process_shebang_file(lines: List[str], header_line: str, comment_start: str) -> str:
    """Process a file with a shebang line."""
    shebang = lines[0]
    remaining_lines = _remove_existing_header(lines[1:], comment_start)
    return f"{shebang}\n{header_line}\n" + "\n".join(remaining_lines)


def _process_html_like_file(lines: List[str], header_line: str, comment_start: str) -> str:
    """Process an HTML-like file."""
    if lines[0].lower().startswith(("<!doctype", "<?xml")):
        first_line = lines[0]
        rest_lines = _remove_existing_header(lines[1:], comment_start)
        return f"{first_line}\n{header_line}\n" + "\n".join(rest_lines)

    lines = _remove_existing_header(lines, comment_start)
    return f"{header_line}\n" + "\n".join(lines)


def _process_regular_file(lines: List[str], header_line: str, comment_start: str) -> str:
    """Process a regular file by inserting the header and preserving existing content."""
    # Remove any existing header if present
    lines = _remove_existing_header(lines, comment_start)

    # Add the new header with a blank line after
    return f"{header_line}\n\n" + "\n".join(lines)


def process_file(file_path: Path, project_root: Path) -> None:
    """Process a single file, adding or updating its header."""
    if not file_path.is_file():
        logging.warning("File not found: %s", file_path)
        return

    comment_style = _get_comment_style(file_path)
    if not comment_style:
        logging.debug("Skipping unsupported file type: %s", file_path)
        return

    comment_start, comment_end = comment_style

    try:
        content = file_path.read_text()
        header = _create_header(file_path, project_root)
        header_line = _create_header_line(comment_start, comment_end, header)
        lines = content.splitlines()

        # If file is empty
        if not lines:
            new_content = _process_empty_file(header_line)
        elif lines[0].startswith("#!"):
            new_content = _process_shebang_file(lines, header_line, comment_start)
        elif _is_html_like(file_path):
            new_content = _process_html_like_file(lines, header_line, comment_start)
        else:
            # Check if file already has our header
            if _has_existing_header(lines, comment_start):
                logging.debug("File already has header: %s", file_path)
                return

            # Add header at the top with blank line after
            new_content = f"{header_line}\n\n{content}"

        # Only write if content has changed
        if new_content != content:
            file_path.write_text(new_content)
            logging.info("Updated header in: %s", file_path)
        else:
            logging.debug("No changes needed for: %s", file_path)

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
