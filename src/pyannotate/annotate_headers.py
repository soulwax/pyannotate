# File: scripts/annotate-headers.py
import os
import logging
from pathlib import Path
from typing import NamedTuple, Optional, Set, List
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class FilePattern(NamedTuple):
    extensions: List[str]
    comment_start: str
    comment_end: Optional[str] = None


# Patterns to identify file types and their comment styles
PATTERNS = [
    FilePattern([".ts", ".js", ".jsx", ".tsx"], "//"),
    FilePattern([".css"], "/*", "*/"),
    FilePattern([".html", ".xml", ".svg"], "<!--", "-->"),
    FilePattern([".py", ".sh", ".bash"], "#"),
    FilePattern([".cpp", ".c", ".hpp", ".h"], "//"),
    FilePattern(
        [".jsonc", ".json5", ".code-workspace", ".eslintrc", ".babelrc", ".prettierrc"],
        "//",
    ),
    FilePattern([".md"], "<!--", "-->"),
    FilePattern([".java"], "//"),
    FilePattern([".go"], "//"),
    FilePattern([".rb"], "#"),
    FilePattern([".php"], "//"),
    FilePattern([".yaml", ".yml"], "#"),
    FilePattern([".dockerfile"], "#"),
    FilePattern([".ini", ".cfg"], "#"),
]

# Directories to ignore during traversal
IGNORED_DIRS: Set[str] = {
    "node_modules",
    "dist",
    "build",
    ".git",
    "coverage",
    "vendor",
    "__pycache__",
    ".idea",
    ".vscode",
}

# Special configuration files and their comment styles
CONFIG_FILES = {
    ".eslintrc": "//",
    ".babelrc": "//",
    ".prettierrc": "//",
    "tsconfig.json": "//",
    "jsconfig.json": "//",
    ".swcrc": "//",
    "docker-compose.yml": "#",
    "Makefile": "#",
    "CMakeLists.txt": "#",
}


def get_special_file_pattern(filename: str) -> Optional[FilePattern]:
    """Check if the file is a special config file that supports comments."""
    if filename in CONFIG_FILES:
        return FilePattern([], CONFIG_FILES[filename])
    return None


def determine_comment_pattern(file_path: Path) -> Optional[FilePattern]:
    """Determine the appropriate comment pattern for a given file."""
    pattern = next((p for p in PATTERNS if file_path.suffix in p.extensions), None)
    return pattern or get_special_file_pattern(file_path.name)


def read_file_content(file_path: Path) -> Optional[str]:
    """Safely read file content."""
    try:
        return file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        logging.warning(f"Failed to read {file_path}: {e}")
        return None


def write_file_content(file_path: Path, content: str) -> None:
    """Safely write file content."""
    try:
        file_path.write_text(content, encoding="utf-8")
        logging.info(f"Updated header in: {file_path}")
    except OSError as e:
        logging.error(f"Failed to write to {file_path}: {e}")


def process_file(file_path: Path, project_root: Path) -> None:
    """Process a single file and add or update its header annotation."""
    pattern = determine_comment_pattern(file_path)
    if not pattern:
        return

    content = read_file_content(file_path)
    if content is None:
        return

    relative_path = str(file_path.relative_to(project_root)).replace(os.sep, "/")
    header_line = f"{pattern.comment_start} File: {relative_path}{pattern.comment_end or ''}"

    header_regex = re.compile(
        rf"^(?:#!.*\n)?{re.escape(pattern.comment_start)}\s*File:\s*[^\n]*{re.escape(pattern.comment_end or '')}\n",
        re.MULTILINE,
    )

    has_shebang = content.startswith("#!")
    shebang_line = content.split("\n", 1)[0] + "\n" if has_shebang else ""

    if header_regex.search(content):
        new_content = header_regex.sub(
            f"{shebang_line}{header_line}\n" if has_shebang else f"{header_line}\n",
            content,
        )
    else:
        new_content = (
            f"{shebang_line}{header_line}\n{content[len(shebang_line):]}"
            if has_shebang
            else f"{header_line}\n{content}"
        )

    if new_content != content:
        write_file_content(file_path, new_content)


def walk_directory(dir_path: Path, project_root: Path) -> None:
    """Recursively walk through directory and process files."""
    for entry in dir_path.iterdir():
        if entry.is_dir():
            if entry.name not in IGNORED_DIRS:
                walk_directory(entry, project_root)
        elif entry.is_file():
            process_file(entry, project_root)


def main() -> None:
    """Main function to initiate the annotation process."""
    project_root = Path.cwd()
    logging.info(f"Starting file annotation from: {project_root}")
    walk_directory(project_root, project_root)
    logging.info("File annotation complete!")


if __name__ == "__main__":
    main()
