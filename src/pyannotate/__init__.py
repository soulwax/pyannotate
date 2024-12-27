"""
PyAnnotate - A tool for annotating files with standardized headers.

This package provides functionality to automatically add or update file headers
in various programming language files.
"""

from .annotate_headers import (
    process_file,
    walk_directory,
    FilePattern,
    PATTERNS,
    IGNORED_DIRS,
    CONFIG_FILES,
)

__version__ = "0.2.1"

__all__ = [
    "process_file",
    "walk_directory",
    "FilePattern",
    "PATTERNS",
    "IGNORED_DIRS",
    "CONFIG_FILES",
]
