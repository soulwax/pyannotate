# File: tests/test_revert.py

"""Tests for the revert functionality."""

import json
from pathlib import Path

import pytest

from annot8.annotate_headers import process_file, walk_directory
from annot8.backup import (
    BACKUP_FILENAME,
    clear_backup,
    load_backup,
    revert_files,
    save_backup,
)
from tests.test_utils import cleanup_test_directory, create_temp_test_directory

# Directory for temporary test files
TEST_DIR = Path("tests/revert_test")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    create_temp_test_directory(TEST_DIR)
    yield
    cleanup_test_directory(TEST_DIR)
    # Also clean up any backup files
    backup_file = TEST_DIR / BACKUP_FILENAME
    if backup_file.exists():
        backup_file.unlink()


def test_save_and_load_backup():
    """Test saving and loading backup files."""
    backup_content = {
        "test.py": "original content",
        "test.js": "original js content",
    }

    save_backup(TEST_DIR, backup_content)

    backup_file = TEST_DIR / BACKUP_FILENAME
    assert backup_file.exists(), "Backup file should be created"

    loaded = load_backup(TEST_DIR)
    assert loaded is not None, "Backup should be loadable"
    assert loaded == backup_content, "Loaded backup should match saved content"


def test_load_backup_nonexistent():
    """Test loading backup when no backup file exists."""
    # Use a different directory that definitely has no backup
    empty_dir = TEST_DIR / "empty"
    empty_dir.mkdir(exist_ok=True)

    loaded = load_backup(empty_dir)
    assert loaded is None, "Should return None when no backup exists"

    empty_dir.rmdir()


def test_revert_files():
    """Test reverting files from backup."""
    # Create test files
    test_file1 = TEST_DIR / "test1.py"
    test_file2 = TEST_DIR / "test2.js"

    original_content1 = "print('original')"
    original_content2 = "console.log('original');"

    # Write original content
    test_file1.write_text(original_content1)
    test_file2.write_text(original_content2)

    # Create backup
    backup_content = {
        "test1.py": original_content1,
        "test2.js": original_content2,
    }
    save_backup(TEST_DIR, backup_content)

    # Modify files
    test_file1.write_text("print('modified')")
    test_file2.write_text("console.log('modified');")

    # Revert
    stats = revert_files(TEST_DIR)

    assert stats["reverted"] == 2, "Should revert 2 files"
    assert stats["missing"] == 0, "No files should be missing"
    assert stats["errors"] == 0, "No errors should occur"

    # Verify files are reverted
    assert test_file1.read_text() == original_content1, "File 1 should be reverted"
    assert test_file2.read_text() == original_content2, "File 2 should be reverted"


def test_revert_files_dry_run():
    """Test dry-run revert without actually reverting."""
    # Create test file
    test_file = TEST_DIR / "test_dry.py"
    original_content = "print('original')"
    modified_content = "print('modified')"

    test_file.write_text(modified_content)

    # Create backup
    backup_content = {"test_dry.py": original_content}
    save_backup(TEST_DIR, backup_content)

    # Dry-run revert
    stats = revert_files(TEST_DIR, dry_run=True)

    assert stats["reverted"] == 1, "Should report 1 file would be reverted"
    assert test_file.read_text() == modified_content, "File should not be modified in dry-run"


def test_revert_missing_file():
    """Test reverting when a file in backup no longer exists."""
    # Create backup for a file that doesn't exist
    backup_content = {"nonexistent.py": "content"}
    save_backup(TEST_DIR, backup_content)

    # Try to revert
    stats = revert_files(TEST_DIR)

    assert stats["reverted"] == 0, "No files should be reverted"
    assert stats["missing"] == 1, "Should report 1 missing file"
    assert stats["errors"] == 0, "No errors should occur"


def test_revert_no_backup():
    """Test reverting when no backup exists."""
    # Clear any existing backup first
    clear_backup(TEST_DIR)
    stats = revert_files(TEST_DIR)

    assert stats["reverted"] == 0, "No files should be reverted"
    assert stats["missing"] == 0, "No missing files"
    assert stats["errors"] == 0, "No errors"


def test_backup_created_during_annotation():
    """Test that backup is created when files are annotated."""
    # Create test file
    test_file = TEST_DIR / "backup_test.py"
    original_content = "print('hello')"
    test_file.write_text(original_content)

    # Process file (should create backup)
    backup_content = {}
    process_file(test_file, TEST_DIR, backup_content=backup_content)

    # Check backup was created
    assert "backup_test.py" in backup_content, "Backup should contain file"
    assert (
        backup_content["backup_test.py"] == original_content
    ), "Backup should have original content"


def test_backup_not_created_in_dry_run():
    """Test that backup is not created during dry-run."""
    test_file = TEST_DIR / "dry_backup_test.py"
    original_content = "print('hello')"
    test_file.write_text(original_content)

    # Process file in dry-run mode
    backup_content = {}
    process_file(test_file, TEST_DIR, dry_run=True, backup_content=backup_content)

    # Check backup was NOT created
    assert len(backup_content) == 0, "Backup should be empty in dry-run"


def test_walk_directory_creates_backup():
    """Test that walk_directory creates backup for modified files."""
    # Create test files
    test_file1 = TEST_DIR / "walk1.py"
    test_file2 = TEST_DIR / "walk2.js"
    test_file1.write_text("print('test1')")
    test_file2.write_text("console.log('test2');")

    # Process directory
    backup_content = {}
    walk_directory(TEST_DIR, TEST_DIR, backup_content=backup_content)

    # Save backup
    if backup_content:
        save_backup(TEST_DIR, backup_content)

    # Verify backup was created
    backup_file = TEST_DIR / BACKUP_FILENAME
    assert backup_file.exists(), "Backup file should exist"

    loaded = load_backup(TEST_DIR)
    assert loaded is not None, "Backup should be loadable"
    assert len(loaded) > 0, "Backup should contain files"


def test_clear_backup():
    """Test clearing backup file."""
    # Create backup
    backup_content = {"test.py": "content"}
    save_backup(TEST_DIR, backup_content)

    backup_file = TEST_DIR / BACKUP_FILENAME
    assert backup_file.exists(), "Backup file should exist"

    # Clear backup
    result = clear_backup(TEST_DIR)
    assert result is True, "Should return True when backup is cleared"
    assert not backup_file.exists(), "Backup file should be deleted"


def test_clear_backup_nonexistent():
    """Test clearing backup when it doesn't exist."""
    result = clear_backup(TEST_DIR)
    assert result is False, "Should return False when no backup exists"


def test_backup_json_structure():
    """Test that backup JSON has correct structure."""
    backup_content = {"test.py": "content"}
    save_backup(TEST_DIR, backup_content)

    backup_file = TEST_DIR / BACKUP_FILENAME
    backup_data = json.loads(backup_file.read_text())

    assert "timestamp" in backup_data, "Backup should have timestamp"
    assert "files" in backup_data, "Backup should have files"
    assert backup_data["files"] == backup_content, "Files should match"


def test_revert_preserves_backup_file():
    """Test that revert keeps the backup file for potential re-revert."""
    test_file = TEST_DIR / "preserve_test.py"
    original_content = "print('original')"
    test_file.write_text(original_content)

    # Create backup
    backup_content = {"preserve_test.py": original_content}
    save_backup(TEST_DIR, backup_content)

    # Modify file
    test_file.write_text("print('modified')")

    # Revert
    revert_files(TEST_DIR)

    # Backup file should still exist
    backup_file = TEST_DIR / BACKUP_FILENAME
    assert backup_file.exists(), "Backup file should be preserved after revert"


def test_backup_relative_paths():
    """Test that backup uses relative paths correctly."""
    # Create nested file
    nested_dir = TEST_DIR / "nested"
    nested_dir.mkdir(exist_ok=True)
    nested_file = nested_dir / "nested.py"
    original_content = "print('nested')"
    nested_file.write_text(original_content)

    # Process and backup
    backup_content = {}
    process_file(nested_file, TEST_DIR, backup_content=backup_content)

    # Check relative path is used (handle both / and \ separators)
    # Pathlib uses native separators, so on Windows it will be backslashes
    expected_paths = ["nested/nested.py", "nested\\nested.py"]
    actual_key = next((k for k in backup_content if "nested" in k and "nested.py" in k), None)
    assert (
        actual_key is not None
    ), f"Should use relative path, got keys: {list(backup_content.keys())}"
    assert backup_content[actual_key] == original_content, "Content should match"

    nested_file.unlink()
    nested_dir.rmdir()


def test_revert_with_subdirectories():
    """Test reverting files in subdirectories."""
    # Create nested structure
    subdir = TEST_DIR / "subdir"
    subdir.mkdir(exist_ok=True)
    subfile = subdir / "subfile.py"
    original_content = "print('sub')"
    subfile.write_text(original_content)

    # Create backup
    backup_content = {"subdir/subfile.py": original_content}
    save_backup(TEST_DIR, backup_content)

    # Modify file
    subfile.write_text("print('modified')")

    # Revert
    stats = revert_files(TEST_DIR)

    assert stats["reverted"] == 1, "Should revert 1 file"
    assert subfile.read_text() == original_content, "File should be reverted"

    subfile.unlink()
    subdir.rmdir()
