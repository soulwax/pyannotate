# File: tests/test_utils.py
# pylint: disable=duplicate-code

"""Shared utilities for tests to reduce code duplication."""

import shutil
from pathlib import Path

from pyannotate.annotate_headers import process_file


def create_temp_test_directory(test_dir: Path) -> None:
    """Create a temporary test directory, removing it if it exists."""
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True)


def cleanup_test_directory(test_dir: Path) -> None:
    """Clean up a test directory."""
    if test_dir.exists():
        shutil.rmtree(test_dir)


def create_test_file_with_header_processing(
    file_path: Path, content: str, project_root: Path
) -> str:
    """Create a test file, process it, and return the processed content."""
    file_path.write_text(content)
    process_file(file_path, project_root)
    return file_path.read_text()


def assert_file_content_unchanged(
    file_path: Path, original_content: str, file_description: str
) -> None:
    """Assert that a file's content has not changed."""
    processed_content = file_path.read_text()
    assert (
        processed_content == original_content
    ), f"{file_description} was modified but should be ignored"


def assert_header_added(file_path: Path, expected_header_start: str, file_description: str) -> None:
    """Assert that a header was added to a file."""
    content = file_path.read_text()
    assert content.startswith(
        expected_header_start
    ), f"Header not added correctly for {file_description}"


def create_standard_test_env(test_dir: Path) -> None:
    """Create a standard test environment with common files."""
    create_temp_test_directory(test_dir)

    # Create basic test files
    (test_dir / "test.py").write_text("print('Hello, World!')")
    (test_dir / "test.js").write_text("console.log('Hello, World!');")
    (test_dir / "test.css").write_text("body { margin: 0; }")

    # Create nested directory
    nested_dir = test_dir / "nested"
    nested_dir.mkdir()
    (nested_dir / "script.sh").write_text('#!/bin/bash\necho "Hello!"')


def prepare_existing_header_js(test_dir: Path, filename: str = "existing_header.js") -> Path:
    """
    Write a JS file with a legacy header used by multiple tests and return its path.
    This centralizes setup to avoid duplicate code across test modules.
    """
    js_file = test_dir / filename
    js_file.write_text(
        """// Old header comment
// Author: Someone
console.log("Hello, World!");"""
    )
    return js_file
