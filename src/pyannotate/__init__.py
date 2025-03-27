# File: src/pyannotate/__init__.py
"""
PyAnnotate - A tool for annotating files with standardized headers.

This package provides functionality to automatically add or update file headers
in various programming language files.
"""

from .annotate_headers import (
    IGNORED_DIRS,
    PATTERNS,
    SPECIAL_FILE_COMMENTS,
    FilePattern,
    process_file,
    walk_directory,
)

__version__ = "0.2.1"

__all__ = [
    "process_file",
    "walk_directory",
    "FilePattern",
    "PATTERNS",
    "IGNORED_DIRS",
    "SPECIAL_FILE_COMMENTS",
]
