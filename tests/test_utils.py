# File: tests/test_utils.py

"""Shared utilities for tests to reduce code duplication."""

"""Shared utilities for tests to reduce code duplication (ohne Duplikate)."""
from pathlib import Path
import shutil

from pyannotate.annotate_headers import process_file
from tests.helpers.components import (
    COMMENT_STYLE_TEST_CASES,
    COMMON_IGNORED_FILES,
    ENV_FILE_NAMES,
    LICENSE_FILE_NAMES,
    WEB_FRAMEWORK_TEMPLATES,
    create_header_test_pattern_files,
    create_web_framework_test_files,
)


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
    assert processed_content == original_content, "{} was modified but should be ignored".format(
        file_description
    )


def assert_header_added(file_path: Path, expected_header_start: str, file_description: str) -> None:
    """Assert that a header was added to a file."""
    content = file_path.read_text()
    assert content.startswith(expected_header_start), "Header not added correctly for {}".format(
        file_description
    )


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
