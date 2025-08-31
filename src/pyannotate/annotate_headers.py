# File: src/pyannotate/annotate_headers.py

"""Core functionality for adding and updating file headers."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class FilePattern:
    """Configuration for file patterns and their comment styles."""

    extensions: List[str]
    comment_start: str
    comment_end: str = ""  # Empty string for single-line comment styles


# Define supported file patterns and their comment styles
PATTERNS = [
    # Original patterns - enhanced with more extensions
    FilePattern([".py", ".sh", ".bash", ".ps1", ".zsh", ".fish"], "#", ""),
    FilePattern(
        [
            ".js",
            ".jsx",
            ".tsx",
            ".ts",
            ".c",
            ".cpp",
            ".h",
            ".hpp",
            ".cs",
            ".java",
            ".swift",
            ".kt",
            ".scala",
        ],
        "//",
        "",
    ),
    FilePattern([".html", ".htm", ".xml", ".ui", ".qrc", ".xaml"], "<!--", "-->"),
    FilePattern([".css", ".scss", ".sass", ".less"], "/*", "*/"),
    # Web frameworks
    FilePattern([".vue", ".svelte"], "<!--", "-->"),  # Vue and Svelte files
    FilePattern([".jsx", ".tsx"], "//", ""),  # React JSX/TSX (already in js group but explicit)
    FilePattern([".astro"], "<!--", "-->"),  # Astro framework
    # Configuration files
    FilePattern([".json5"], "//", ""),  # JSON5
    FilePattern([".toml", ".conf", ".cfg", ".ini"], "#", ""),  # Configuration files
    FilePattern([".properties"], "#", ""),  # Java properties
    FilePattern([".yaml", ".yml"], "#", ""),  # YAML files
    # Script files
    FilePattern([".pl", ".pm"], "#", ""),  # Perl
    FilePattern([".rb"], "#", ""),  # Ruby
    FilePattern([".lua"], "--", ""),  # Lua
    FilePattern([".tcl"], "#", ""),  # Tcl
    FilePattern([".php"], "//", ""),  # PHP (can also use # but // is more common)
    # Shell and script enhancements
    FilePattern([".cmd", ".bat"], "REM", ""),  # Windows batch
    FilePattern(
        [".ps1", ".psm1", ".psd1"], "#", ""
    ),  # PowerShell (already in first group but explicit)
    # Systems programming
    FilePattern([".go"], "//", ""),  # Go
    FilePattern([".rs"], "//", ""),  # Rust
    FilePattern([".zig"], "//", ""),  # Zig
    # Functional languages
    FilePattern([".ex", ".exs"], "#", ""),  # Elixir
    FilePattern([".erl", ".hrl"], "%", ""),  # Erlang
    FilePattern([".hs"], "--", ""),  # Haskell
    FilePattern([".lisp", ".cl", ".el"], ";;", ""),  # Lisp family
    # Data science
    FilePattern([".r", ".R"], "#", ""),  # R
    FilePattern([".jl"], "#", ""),  # Julia
    # Markup and documentation
    FilePattern([".rst"], ".. ", ""),  # reStructuredText
    # Database
    FilePattern([".sql"], "--", ""),  # SQL
    # Qt specific files
    FilePattern([".pro", ".pri"], "#", ""),  # Qt project files
    FilePattern([".ui", ".qrc"], "<!--", "-->"),  # Qt UI and resource files
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
    "build",
    "dist",
    "icon",
    "OtherPic",
    "donate",
    ".next",  # Next.js build
    ".nuxt",  # Nuxt.js build
    ".output",  # Nuxt.js 3 build
    "out",  # Common build output
    ".cache",  # Various caches
    ".parcel-cache",  # Parcel bundler cache
    ".yarn",  # Yarn cache
    ".pnpm-store",  # PNPM store
    "coverage",  # Test coverage reports
    "vendor",  # PHP/Composer vendor directory
    "bower_components",  # Legacy Bower components
}

# Define specific files to completely ignore
IGNORED_FILES: Set[str] = {
    # Configuration files that shouldn't have headers
    ".prettierrc",
    ".eslintrc",
    ".babelrc",
    ".stylelintrc",
    ".browserslistrc",
    ".nvmrc",
    ".npmrc",
    ".yarnrc",
    ".editorconfig",
    ".gitattributes",
    ".gitmodules",
    ".hgignore",
    ".hgsub",
    ".hgsubstate",
    ".hgtags",
    "requirements.txt",
    "requirements-dev.txt",
    # Lock files and auto-generated files
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Pipfile.lock",
    "poetry.lock",
    "Cargo.lock",
    "go.sum",
    # Other config files without extensions
    "Procfile",
    "Brewfile",
    "Vagrantfile",
    "Rakefile",
    # Files that might break with headers
    ".env.example",
    ".env.local",
    ".env.development",
    ".env.production",
    # Special files
    "LICENSE",
    "COPYING",
    "NOTICE",
    "AUTHORS",
    "CONTRIBUTORS",
    "CHANGELOG",
    "HISTORY",
    # IDE and editor files
    ".vscode/settings.json",
    ".idea/workspace.xml",
    ".idea/modules.xml",
}

# Define binary file extensions to skip
BINARY_EXTENSIONS = {
    # Executables and libraries
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".bin",
    ".a",
    ".lib",
    ".obj",
    ".o",
    # Images
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".bmp",
    ".tiff",
    ".webp",
    ".avif",
    # Audio
    ".mp3",
    ".wav",
    ".ogg",
    ".flac",
    ".aac",
    ".m4a",
    # Video
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
    ".flv",
    ".wmv",
    # Archives
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
    # Documents
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    # Qt binary formats
    ".qm",
    ".qmlc",
    ".jsc",
    # Other binary formats
    ".pyc",
    ".pyo",
    ".pyd",
    ".class",
    ".jar",
    ".war",
    ".whl",
    # Database files
    ".db",
    ".sqlite",
    ".sqlite3",
    ".mdb",
    # Font files
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
    ".eot",
}

# Define special config files and their comment styles as (start, end) tuples
SPECIAL_FILE_COMMENTS: Dict[str, Tuple[str, str]] = {
    # Original entries
    ".gitignore": ("#", ""),
    ".dockerignore": ("#", ""),
    ".env": ("#", ""),
    "Makefile": ("#", ""),
    "CMakeLists.txt": ("#", ""),
    ".clang-format": ("#", ""),
    ".editorconfig": ("#", ""),
    ".gitlab-ci.yml": ("#", ""),
    ".travis.yml": ("#", ""),
    ".coveragerc": ("#", ""),
    ".flake8": ("#", ""),
    ".gitattributes": ("#", ""),
    ".gitmodules": ("#", ""),
    ".hgignore": ("#", ""),
    ".hgsub": ("#", ""),
    ".hgsubstate": ("#", ""),
    ".hgtags": ("#", ""),
    ".npmignore": ("#", ""),
    "Dockerfile": ("#", ""),
    "docker-compose.yml": ("#", ""),
    "docker-compose.yaml": ("#", ""),
    "Pipfile": ("#", ""),
    "Pipfile.lock": ("#", ""),
    "pyproject.toml": ("#", ""),
    "setup.cfg": ("#", ""),
    "setup.py": ("#", ""),
    "requirements.txt": ("#", ""),
    "requirements-dev.txt": ("#", ""),
    # Additional config files
    "package.json": ("//", ""),  # NPM package file
    "tsconfig.json": ("//", ""),  # TypeScript config
    "jsconfig.json": ("//", ""),  # JavaScript config
    ".eslintrc.json": ("//", ""),  # ESLint config
    ".prettierrc": ("//", ""),  # Prettier config
    ".stylelintrc": ("//", ""),  # Stylelint config
    ".babelrc": ("//", ""),  # Babel config
    ".browserslistrc": ("#", ""),  # Browserslist config
    ".nvmrc": ("#", ""),  # Node Version Manager
    ".npmrc": ("#", ""),  # NPM config
    ".yarnrc": ("#", ""),  # Yarn config
    "yarn.lock": ("#", ""),  # Yarn lock file
    "package-lock.json": ("//", ""),  # NPM lock file
    "pnpm-lock.yaml": ("#", ""),  # PNPM lock file
    "composer.json": ("//", ""),  # PHP Composer
    "Gemfile": ("#", ""),  # Ruby gems
    "Gemfile.lock": ("#", ""),  # Ruby gems lock
    ".rubocop.yml": ("#", ""),  # Ruby linter
    "go.mod": ("//", ""),  # Go modules
    "go.sum": ("//", ""),  # Go checksum
    "Cargo.toml": ("#", ""),  # Rust cargo
    "Cargo.lock": ("#", ""),  # Rust cargo lock
    ".htaccess": ("#", ""),  # Apache config
    "nginx.conf": ("#", ""),  # Nginx config
    "webpack.config.js": ("//", ""),  # Webpack config
    "rollup.config.js": ("//", ""),  # Rollup config
    "vite.config.js": ("//", ""),  # Vite config
    "next.config.js": ("//", ""),  # Next.js config
    "nuxt.config.js": ("//", ""),  # Nuxt.js config
    "svelte.config.js": ("//", ""),  # Svelte config
    "astro.config.mjs": ("//", ""),  # Astro config
    "tailwind.config.js": ("//", ""),  # Tailwind CSS
    "postcss.config.js": ("//", ""),  # PostCSS
    "Rakefile": ("#", ""),  # Ruby make-like
    ".clang-tidy": ("#", ""),
    ".github": ("#", ""),  # GitHub config directory
    ".drone.yml": ("#", ""),  # Drone CI
    ".circleci": ("#", ""),  # CircleCI config
    ".appveyor.yml": ("#", ""),  # AppVeyor CI
}


def _normalize_path(path: str) -> str:
    """Normalize path separators to forward slashes."""
    return path.replace(os.sep, "/")


def _create_header(file_path: Path, project_root: Path) -> str:
    """Create the header content for a file."""
    relative_path = os.path.relpath(file_path, project_root)
    return f"File: {_normalize_path(relative_path)}"


def _is_special_xml_file(file_path: Path) -> bool:
    """
    Check if file is a special XML-based file that needs declaration preservation.
    Enhanced to include web framework files like Vue and Svelte.
    """
    xml_extensions = {
        # HTML/XML family
        ".html",
        ".htm",
        ".xhtml",
        ".xml",
        ".ui",
        ".qrc",
        ".ts",
        # Web component frameworks
        ".vue",
        ".svelte",
        ".astro",
        ".wxml",
        ".blade.php",
        # Documentation formats
        ".mdx",
        ".jsx",
        ".tsx",  # JSX can sometimes have XML-like structure
    }
    return file_path.suffix.lower() in xml_extensions


def _process_empty_file(header_line: str) -> str:
    """Process an empty file (ensure trailing newline)."""
    return f"{header_line}\n"


def _create_header_line(comment_start: str, comment_end: str, header: str) -> str:
    """Create a properly formatted header line with comments."""
    if comment_end:
        return f"{comment_start} {header} {comment_end}"
    return f"{comment_start} {header}"


def _has_existing_header(lines: List[str], comment_start: str, start_index: int = 0) -> bool:
    """
    Check if file has an existing header at the specified start index.
    This enhanced version detects various header patterns, not just our specific format.
    """
    if not lines[start_index:]:
        return False

    # Check first few lines for existing headers - these are definite indicators
    header_indicators = [
        f"{comment_start} File:",  # Our standard format
        f"{comment_start}File:",  # No space after comment
        f"{comment_start} file:",  # Lowercase "file"
        f"{comment_start} Filename:",  # Alternative format
        f"{comment_start} @file",  # JSDoc style
        f"{comment_start} Source:",  # Alternative format
        f"{comment_start} Path:",  # Alternative format
    ]

    # Look for these indicators only in the first line or two
    for i in range(start_index, min(start_index + 2, len(lines))):
        line = lines[i].strip()
        if any(line.startswith(indicator) for indicator in header_indicators):
            return True

    # If we reach here, we didn't find a primary header indicator
    return False


def _merge_headers(
    existing_header: str, new_header: str, comment_start: str, comment_end: str
) -> str:
    """
    Intelligently merge an existing header with our new header.
    Preserves useful information from the existing header while ensuring our format is used.

    Args:
        existing_header: The existing header content
        new_header: Our new header content
        comment_start: Comment start marker
        comment_end: Comment end marker

    Returns:
        Merged header string
    """
    # Extract file path from our new header
    file_path = new_header.replace("File:", "").strip()

    # Split existing header into lines
    existing_lines = existing_header.strip().split("\n")

    # Create our standard header line
    standard_header = f"{comment_start} File: {file_path}"
    if comment_end:
        standard_header += f" {comment_end}"

    # Identify header line vs. metadata lines
    metadata_lines: List[str] = []

    for line in existing_lines:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue

        # Check if this is a file path line (to exclude)
        is_file_path_line = False
        for keyword in ["file:", "filename:", "path:", "@file"]:
            if keyword in line.lower() and line.lower().index(keyword) < 15:
                is_file_path_line = True
                break

        # If not a file path line, treat as metadata if it starts with a comment
        if not is_file_path_line and line.startswith(comment_start):
            # Analyze the line to extract metadata
            metadata_text = line[len(comment_start) :].strip()
            if comment_end and comment_end in metadata_text:
                metadata_text = metadata_text[: metadata_text.rfind(comment_end)].strip()

            # Only keep non-empty metadata
            if metadata_text:
                # Rebuild the comment with our style
                if comment_end:
                    metadata_lines.append(f"{comment_start} {metadata_text} {comment_end}")
                else:
                    metadata_lines.append(f"{comment_start} {metadata_text}")

    # Build the new header with our standard format followed by preserved metadata
    if metadata_lines:
        result = standard_header + "\n" + "\n".join(metadata_lines)
    else:
        result = standard_header

    return result


def _remove_existing_header(
    lines: List[str], comment_start: str, start_index: int = 0
) -> List[str]:
    """
    Remove existing header if present, starting from the specified index.
    This enhanced version handles various header formats and multi-line headers.
    """
    if not _has_existing_header(lines, comment_start, start_index):
        return lines

    # If we have a header, let's identify its boundaries
    header_start = start_index
    header_end = start_index

    # Look for the start of actual content after the header
    # Skip empty lines and lines that look like header continuations
    for i in range(start_index + 1, min(len(lines), start_index + 10)):
        line = lines[i].strip()
        # If empty line or starts with comment marker, consider it part of the header
        if not line or line.startswith(comment_start):
            header_end = i
        else:
            # We found the first line of actual content
            break

    # Construct the new lines without the header
    return lines[:header_start] + lines[header_end + 1 :]


def _detect_header_pattern(file_path: Path) -> Optional[Tuple[str, str, str]]:
    """
    Analyze a file to detect any existing header pattern.

    Returns:
        Tuple containing (detected comment start, detected comment end, header pattern)
        or None if no pattern is detected.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()[:10]]  # Read first 10 lines

        if not lines:
            return None

        # Common comment markers
        markers = [
            ("#", ""),
            ("//", ""),
            ("/*", "*/"),
            ("<!--", "-->"),
            ("%", ""),  # LaTeX
            (";", ""),  # Assembly, INI
            ("--", ""),  # SQL, Haskell
            ("REM", ""),  # Batch
        ]

        # Check each marker against the first few non-empty lines
        for start, end in markers:
            for line in lines:
                if not line:
                    continue

                # Check if line starts with comment marker and contains header-like text
                if line.startswith(start) and any(
                    keyword in line.lower()
                    for keyword in ["file", "source", "path", "filename", "@file"]
                ):
                    # Extract the pattern (e.g., "File: ", "Filename: ")
                    text = line[len(start) :].strip()
                    for keyword in ["file:", "source:", "path:", "filename:", "@file"]:
                        if keyword in text.lower():
                            idx = text.lower().find(keyword)
                            pattern = text[: idx + len(keyword)]
                            return start, end, pattern

        return None

    except (UnicodeDecodeError, IOError):
        return None


def _strip_leading_blank_lines(lines: List[str]) -> List[str]:
    """Remove any leading blank lines from a list of lines."""
    for i, line in enumerate(lines):
        if line.strip():
            return lines[i:]
    return []


def _compose_with_header_block(header_block: str, body_lines: List[str]) -> str:
    """
    Compose a full file from a header block (one or multiple header lines)
    and the remaining body lines, ensuring:
    - exactly one blank line between header and body (if body exists)
    - trailing newline at EOF
    """
    hb = header_block.rstrip("\n")
    body = _strip_leading_blank_lines(body_lines)
    if body:
        result = f"{hb}\n\n" + "\n".join(body)
    else:
        result = f"{hb}\n"
    if not result.endswith("\n"):
        result += "\n"
    return result


def _process_shebang_file(lines: List[str], header_line: str, comment_start: str) -> str:
    """Process a file with a shebang line."""
    shebang = lines[0]
    remaining_lines = _remove_existing_header(lines[1:], comment_start)
    rest = _compose_with_header_block(header_line, remaining_lines)
    # Prepend shebang (compose already ensures trailing newline)
    result = f"{shebang}\n{rest}"
    if not result.endswith("\n"):
        result += "\n"
    return result


def _process_xml_like_file(lines: List[str], header_line: str, comment_start: str) -> str:
    """
    Process XML-like files while preserving declarations.
    Enhanced version to better handle web framework templates.
    """
    if not lines:
        return _process_empty_file(header_line)

    # Store all declaration lines and document type definitions
    declarations: List[str] = []
    content_start = 0

    # Identify special top lines that must be preserved at the very beginning
    for i, line in enumerate(lines):
        line_stripped = line.strip().lower()
        # Look for XML declarations, DOCTYPE definitions, and processing instructions
        if (
            line_stripped.startswith(("<?xml", "<!doctype", "<?php", "<%", "<%=", "<%@"))
            or line_stripped.startswith("<script setup")
            or line_stripped.startswith("<template")
        ):
            declarations.append(lines[i])
            content_start = i + 1
        else:
            # Stop when we hit non-declaration content
            break

    # If we have declarations, preserve them at the start
    if declarations:
        # Remove any existing header from remaining content
        remaining_lines = _remove_existing_header(lines[content_start:], comment_start)
        composed = _compose_with_header_block(header_line, remaining_lines)
        # Prepend declarations (each is already a single line)
        result = "\n".join(declarations) + "\n" + composed
        if not result.endswith("\n"):
            result += "\n"
        return result

    # If no declarations, treat as regular file with header at top
    remaining_lines = _remove_existing_header(lines, comment_start)
    return _compose_with_header_block(header_line, remaining_lines)


def _process_web_framework_file(
    file_path: Path, lines: List[str], header_line: str, comment_start: str
) -> str:
    """
    Special handling for web framework files like Vue, Svelte, etc.
    These can have mixed content with template, script, and style sections.
    """
    # Identify the file type
    suffix = file_path.suffix.lower()

    # For Vue and Svelte files, ensure header placement is optimal
    if suffix in {".vue", ".svelte"}:
        # Check for template/script block patterns
        has_template = any("<template" in line.lower() for line in lines[:10])
        has_script_setup = any("<script setup" in line.lower() for line in lines[:15])

        if has_template or has_script_setup:
            # For Vue files with template or script setup, use special XML processing
            return _process_xml_like_file(lines, header_line, comment_start)

    # Default back to regular header placement for other cases
    remaining_lines = _remove_existing_header(lines, comment_start)
    return _compose_with_header_block(header_line, remaining_lines)


def is_binary(file_path: Path) -> bool:
    """Check if a file is binary."""
    # Check extension first for efficiency
    if file_path.suffix.lower() in BINARY_EXTENSIONS:
        return True

    try:
        with open(file_path, "rb") as f:
            # Read first 1024 bytes to determine if file is binary
            chunk = f.read(1024)
            return b"\0" in chunk  # Binary files typically contain null bytes
    except OSError:
        return True


def _is_qt_translation_file(file_path: Path) -> bool:
    """
    Determine if a .ts file is a Qt translation file (XML-based) or TypeScript file.
    Qt translation files typically have XML structure with TS root element.
    """
    if file_path.suffix.lower() != ".ts":
        return False

    try:
        content = file_path.read_text(encoding="utf-8")
        content_lower = content.lower()
        # Check for XML declaration or DOCTYPE TS or <TS tags
        return (
            "<?xml" in content_lower
            or "<!doctype ts" in content_lower
            or "<ts " in content_lower
            or "<ts>" in content_lower
        )
    except (OSError, UnicodeDecodeError):
        # If we can't read the file or encounter an error, default to TypeScript
        return False


def _get_comment_style(file_path: Path) -> Optional[Tuple[str, str]]:
    """
    Determine the appropriate comment style for a given file.
    Enhanced to handle web framework files and more formats.
    """
    # Check if it's a special config file
    if file_path.name in SPECIAL_FILE_COMMENTS:
        return SPECIAL_FILE_COMMENTS[file_path.name]

    # Web framework special cases
    if file_path.suffix.lower() == ".vue":
        return ("<!--", "-->")  # Vue files use HTML comments

    if file_path.suffix.lower() == ".svelte":
        return ("<!--", "-->")  # Svelte files use HTML comments

    if file_path.suffix.lower() == ".astro":
        return ("<!--", "-->")  # Astro files use HTML comments

    # Special handling for .ts files
    if file_path.suffix.lower() == ".ts":
        if _is_qt_translation_file(file_path):
            return ("<!--", "-->")  # XML style for Qt translation files
        return ("//", "")  # JavaScript style for TypeScript files

    # Check extension patterns
    for pattern in PATTERNS:
        if any(str(file_path).lower().endswith(ext) for ext in pattern.extensions):
            return (pattern.comment_start, pattern.comment_end)

    # Last resort: try to detect from file content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()

            # If it starts with common comment markers, use that
            if first_line.startswith("//"):
                return ("//", "")
            if first_line.startswith("#"):
                return ("#", "")
            if first_line.startswith("/*"):
                return ("/*", "*/")
            if first_line.startswith("<!--"):
                return ("<!--", "-->")
    except (UnicodeDecodeError, IOError):
        pass

    return None


def _collect_metadata_lines(lines: List[str], comment_start: str) -> List[str]:
    """Collect metadata lines from the beginning of a file."""
    metadata_lines: List[str] = []
    in_metadata_block = False

    # Look at up to the first 10 lines for metadata
    for i in range(min(10, len(lines))):
        line = lines[i].strip()
        # Skip empty lines
        if not line:
            continue

        # If line starts with a comment and contains metadata
        if line.startswith(comment_start) and any(
            keyword in line.lower()
            for keyword in ["author:", "version:", "copyright:", "created:", "description:"]
        ):
            metadata_lines.append(line)
            in_metadata_block = True
        elif in_metadata_block and line.startswith(comment_start):
            # Continue collecting metadata if we're in a block of commented lines
            metadata_lines.append(line)
        else:
            # Stop once we hit non-comment or non-metadata content
            if in_metadata_block:
                break

    return metadata_lines


def _should_skip_path(file_path: Path) -> bool:
    """Centralize skip logic to reduce statements in process_file."""
    if not file_path.is_file():
        logging.warning("File not found: %s", file_path)
        return True
    if file_path.suffix.lower() in {".md", ".markdown", ".json"} or (
        file_path.name.lower() == "license" and not file_path.suffix
    ):
        logging.debug("Skipping documentation file: %s", file_path)
        return True
    if file_path.name in IGNORED_FILES:
        logging.debug("Skipping ignored file: %s", file_path)
        return True
    if file_path.suffix.lower() in BINARY_EXTENSIONS or is_binary(file_path):
        logging.debug("Skipping binary file: %s", file_path)
        return True
    return False


def _read_text_best_effort(file_path: Path) -> str:
    """Read text using UTF-8 with fallback to system default."""
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return file_path.read_text()


def _determine_new_content(
    file_path: Path,
    content: str,
    comment_start: str,
    comment_end: str,
    header_line: str,
) -> Optional[str]:
    """Pure function to compute new content for a file given its current content."""
    lines = content.splitlines()
    metadata_lines = _collect_metadata_lines(lines, comment_start)

    if not lines:
        return _process_empty_file(header_line)
    if lines[0].startswith("#!"):
        return _process_shebang_file(lines, header_line, comment_start)
    if _is_special_xml_file(file_path):
        return _process_xml_like_file(lines, header_line, comment_start)
    if file_path.suffix.lower() in {".vue", ".svelte", ".astro"}:
        return _process_web_framework_file(file_path, lines, header_line, comment_start)

    if _has_existing_header(lines, comment_start):
        existing_pattern = _detect_header_pattern(file_path)
        if existing_pattern:
            detected_start, _detected_end, _pattern = existing_pattern
            # capture up to 10 header lines
            header_lines: List[str] = []
            for i in range(min(10, len(lines))):
                line = lines[i].strip()
                if line and line.startswith(comment_start):
                    header_lines.append(lines[i])
                elif not line:
                    continue
                else:
                    break
            existing_header = "\n".join(header_lines)
            merged_header = _merge_headers(
                existing_header, header_line[len(comment_start) + 1 :], comment_start, comment_end
            )
            remaining_lines = _remove_existing_header(lines, detected_start)
            return _compose_with_header_block(merged_header, remaining_lines)
        # pattern not detectable: bail out
        logging.debug("File already has header: %s", file_path)
        return None

    if metadata_lines:
        combined_header = header_line + "\n" + "\n".join(metadata_lines)
        remaining_lines = [
            line for line in lines if line.strip() not in [l.strip() for l in metadata_lines]
        ]
        return _compose_with_header_block(combined_header, remaining_lines)

    # default: put header on top (ensure one blank line and trailing newline)
    if content.strip():
        return _compose_with_header_block(header_line, content.splitlines())
    return _process_empty_file(header_line)


def process_file(file_path: Path, project_root: Path) -> None:
    """Process a single file, adding or updating its header."""
    if _should_skip_path(file_path):
        return

    comment_style = _get_comment_style(file_path)
    if not comment_style:
        logging.debug("Skipping unsupported file type: %s", file_path)
        return

    comment_start, comment_end = comment_style

    try:
        content = _read_text_best_effort(file_path)
        header = _create_header(file_path, project_root)
        header_line = _create_header_line(comment_start, comment_end, header)
        new_content = _determine_new_content(
            file_path, content, comment_start, comment_end, header_line
        )

        if new_content is not None and new_content != content:
            file_path.write_text(new_content, encoding="utf-8")
            logging.info("Updated header in: %s", file_path)
        else:
            logging.debug("No changes needed for: %s", file_path)
    except (OSError, UnicodeDecodeError) as e:
        logging.debug("Failed to process %s: %s", file_path, e)


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
