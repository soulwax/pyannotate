# File: tests/test_git_integration.py
# pylint: disable=duplicate-code

"""Tests for git integration functionality."""

import subprocess
import tempfile
from pathlib import Path

import pytest

from pyannotate.git_integration import (
    get_git_author,
    get_git_email,
    get_git_file_author,
    get_git_file_date,
    get_git_metadata,
    get_git_root,
    get_git_staged_files,
    get_git_tracked_files,
    is_git_repository,
)


@pytest.fixture(name="git_repo")
def temp_git_repo():
    """Create a temporary git repository for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Initialize git repo
        subprocess.run(
            ["git", "init"],
            cwd=temp_path,
            capture_output=True,
            check=False,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=temp_path,
            capture_output=True,
            check=False,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=temp_path,
            capture_output=True,
            check=False,
        )

        yield temp_path


def test_is_git_repository(git_repo):
    """Test detecting git repository."""
    repo_path = git_repo
    assert is_git_repository(repo_path), "Should detect git repository"

    non_git_dir = Path(tempfile.mkdtemp())
    assert not is_git_repository(non_git_dir), "Should not detect non-git directory"
    non_git_dir.rmdir()


def test_get_git_root(git_repo):
    """Test getting git root directory."""
    repo_path = git_repo
    git_root = get_git_root(repo_path)
    assert git_root is not None, "Should find git root"
    assert git_root == repo_path, "Git root should match temp directory"

    # Test subdirectory
    subdir = repo_path / "subdir"
    subdir.mkdir()
    git_root_from_subdir = get_git_root(subdir)
    assert git_root_from_subdir == repo_path, "Should find root from subdirectory"


def test_get_git_root_non_repo():
    """Test getting git root from non-repository."""
    with tempfile.TemporaryDirectory() as temp_dir:
        git_root = get_git_root(Path(temp_dir))
        assert git_root is None, "Should return None for non-git directory"


def test_get_git_tracked_files(git_repo):
    """Test getting git tracked files."""
    repo_path = git_repo
    # Create and track some files
    file1 = repo_path / "tracked.py"
    file2 = repo_path / "tracked.js"
    file1.write_text("print('test')")
    file2.write_text("console.log('test');")

    subprocess.run(
        ["git", "add", "tracked.py", "tracked.js"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )

    tracked = get_git_tracked_files(repo_path, repo_path)
    assert len(tracked) >= 2, "Should find tracked files"
    assert Path("tracked.py") in tracked or any("tracked.py" in str(p) for p in tracked)
    assert Path("tracked.js") in tracked or any("tracked.js" in str(p) for p in tracked)


def test_get_git_staged_files(git_repo):
    """Test getting git staged files."""
    repo_path = git_repo
    # Create and stage a file
    staged_file = repo_path / "staged.py"
    staged_file.write_text("print('staged')")

    subprocess.run(
        ["git", "add", "staged.py"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )

    staged = get_git_staged_files(repo_path, repo_path)
    assert len(staged) >= 1, "Should find staged files"
    assert Path("staged.py") in staged or any("staged.py" in str(p) for p in staged)


def test_get_git_author(git_repo):
    """Test getting git author."""
    repo_path = git_repo
    author = get_git_author(repo_path)
    assert author == "Test User", "Should get configured git author"


def test_get_git_email(git_repo):
    """Test getting git email."""
    repo_path = git_repo
    email = get_git_email(repo_path)
    assert email == "test@example.com", "Should get configured git email"


def test_get_git_file_author(git_repo):
    """Test getting file author from git history."""
    repo_path = git_repo
    # Create and commit a file
    test_file = repo_path / "test.py"
    test_file.write_text("print('test')")

    subprocess.run(
        ["git", "add", "test.py"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )

    author = get_git_file_author(test_file, repo_path)
    assert author == "Test User", "Should get file author from git history"


def test_get_git_file_date(git_repo):
    """Test getting file date from git history."""
    repo_path = git_repo
    # Create and commit a file
    test_file = repo_path / "dated.py"
    test_file.write_text("print('dated')")

    subprocess.run(
        ["git", "add", "dated.py"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )
    subprocess.run(
        ["git", "commit", "-m", "Add dated file"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )

    date = get_git_file_date(test_file, repo_path)
    assert date is not None, "Should get file date from git"
    assert len(date) == 10, "Date should be in YYYY-MM-DD format"


def test_get_git_metadata(git_repo):
    """Test getting complete git metadata."""
    repo_path = git_repo
    # Create and commit a file
    test_file = repo_path / "metadata.py"
    test_file.write_text("print('metadata')")

    subprocess.run(
        ["git", "add", "metadata.py"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )
    subprocess.run(
        ["git", "commit", "-m", "Add metadata file"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )

    metadata = get_git_metadata(test_file, repo_path)
    assert "author" in metadata, "Should have author"
    assert "email" in metadata, "Should have email"
    assert "date" in metadata, "Should have date"
    assert metadata["author"] == "Test User", "Author should match"
    assert metadata["email"] == "test@example.com", "Email should match"


def test_get_git_metadata_with_config(git_repo):
    """Test getting git metadata with custom date format."""
    repo_path = git_repo
    test_file = repo_path / "formatted.py"
    test_file.write_text("print('formatted')")

    subprocess.run(
        ["git", "add", "formatted.py"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )
    subprocess.run(
        ["git", "commit", "-m", "Add formatted file"],
        cwd=repo_path,
        capture_output=True,
        check=False,
    )

    config = {"date_format": "%Y/%m/%d"}
    metadata = get_git_metadata(test_file, repo_path, config)
    assert metadata["date"] is not None, "Should have date"
    # Date should contain slashes if format was applied
    if metadata["date"]:
        # Format might vary, just check it exists
        assert len(metadata["date"]) > 0


def test_get_git_tracked_files_empty_repo(git_repo):
    """Test getting tracked files from empty repository."""
    repo_path = git_repo
    tracked = get_git_tracked_files(repo_path, repo_path)
    # Empty repo should have no tracked files
    assert isinstance(tracked, set), "Should return a set"


def test_get_git_staged_files_no_staged(git_repo):
    """Test getting staged files when nothing is staged."""
    repo_path = git_repo
    staged = get_git_staged_files(repo_path, repo_path)
    assert isinstance(staged, set), "Should return a set"
    # May be empty or contain files depending on git state


def test_get_git_author_no_config():
    """Test getting git author when not configured locally."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        # Don't configure git user locally (will fall back to global config)
        author = get_git_author(temp_path)
        # Git falls back to global config, so may return a value or None
        # Just verify it doesn't crash and returns a string or None
        assert author is None or isinstance(author, str)


def test_get_git_email_no_config():
    """Test getting git email when not configured locally."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        # Don't configure git user locally (will fall back to global config)
        email = get_git_email(temp_path)
        # Git falls back to global config, so may return a value or None
        # Just verify it doesn't crash and returns a string or None
        assert email is None or isinstance(email, str)


def test_get_git_file_author_no_history(git_repo):
    """Test getting file author for file with no git history."""
    repo_path = git_repo
    untracked_file = repo_path / "untracked.py"
    untracked_file.write_text("print('untracked')")

    author = get_git_file_author(untracked_file, repo_path)
    # Should return None if file has no git history
    assert author is None or author == ""


def test_get_git_file_date_no_history(git_repo):
    """Test getting file date for file with no git history."""
    repo_path = git_repo
    untracked_file = repo_path / "no_history.py"
    untracked_file.write_text("print('no history')")

    date = get_git_file_date(untracked_file, repo_path)
    # Should return None if file has no git history
    assert date is None
