# File: src/pyannotate/git_integration.py

"""Git integration for PyAnnotate."""

import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    from pathspec import PathSpec
    from pathspec.patterns import GitWildMatchPattern

    PATHSPEC_AVAILABLE = True
except ImportError:
    PATHSPEC_AVAILABLE = False


def is_git_repository(directory: Path) -> bool:
    """
    Check if a directory is a git repository.

    Args:
        directory: Directory to check

    Returns:
        True if directory is a git repository, False otherwise
    """
    git_dir = directory / ".git"
    return git_dir.exists() and (git_dir.is_dir() or git_dir.is_file())


def get_git_root(directory: Path) -> Optional[Path]:
    """
    Get the root directory of the git repository.

    Args:
        directory: Directory to start searching from

    Returns:
        Path to git root, or None if not in a git repository
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def get_git_tracked_files(git_root: Path, relative_to: Optional[Path] = None) -> Set[Path]:
    """
    Get all files tracked by git.

    Args:
        git_root: Root of the git repository
        relative_to: Directory to make paths relative to (default: git_root)

    Returns:
        Set of file paths (relative to relative_to or git_root)
    """
    if relative_to is None:
        relative_to = git_root

    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if result.returncode != 0:
            return set()

        tracked_files = set()
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            file_path = git_root / line
            try:
                relative_path = file_path.relative_to(relative_to)
                if file_path.exists() and file_path.is_file():
                    tracked_files.add(relative_path)
            except ValueError:
                # File is outside relative_to directory
                continue

        return tracked_files
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        logging.debug("Failed to get git tracked files: %s", e)
        return set()


def get_git_staged_files(git_root: Path, relative_to: Optional[Path] = None) -> Set[Path]:
    """
    Get all files staged for commit.

    Args:
        git_root: Root of the git repository
        relative_to: Directory to make paths relative to (default: git_root)

    Returns:
        Set of staged file paths (relative to relative_to or git_root)
    """
    if relative_to is None:
        relative_to = git_root

    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if result.returncode != 0:
            return set()

        staged_files = set()
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            file_path = git_root / line
            try:
                relative_path = file_path.relative_to(relative_to)
                if file_path.exists() and file_path.is_file():
                    staged_files.add(relative_path)
            except ValueError:
                continue

        return staged_files
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        logging.debug("Failed to get git staged files: %s", e)
        return set()


def get_gitignore_patterns(git_root: Path) -> Optional[PathSpec]:
    """
    Load .gitignore patterns from the repository.

    Args:
        git_root: Root of the git repository

    Returns:
        PathSpec object with gitignore patterns, or None if pathspec not available
    """
    if not PATHSPEC_AVAILABLE:
        return None

    gitignore_path = git_root / ".gitignore"
    patterns: List[str] = []

    # Read .gitignore
    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                patterns.extend(f.read().splitlines())
        except (OSError, UnicodeDecodeError):
            pass

    # Also check .git/info/exclude
    exclude_path = git_root / ".git" / "info" / "exclude"
    if exclude_path.exists():
        try:
            with open(exclude_path, "r", encoding="utf-8") as f:
                patterns.extend(f.read().splitlines())
        except (OSError, UnicodeDecodeError):
            pass

    if not patterns:
        return None

    # Filter out comments and empty lines
    filtered_patterns = [p.strip() for p in patterns if p.strip() and not p.strip().startswith("#")]

    if not filtered_patterns:
        return None

    try:
        return PathSpec.from_lines(GitWildMatchPattern, filtered_patterns)
    except (ValueError, TypeError, AttributeError):
        return None


def is_gitignored(file_path: Path, git_root: Path, gitignore_spec: Optional[PathSpec]) -> bool:
    """
    Check if a file is ignored by git.

    Args:
        file_path: File to check (must be relative to git_root)
        git_root: Root of the git repository
        file_path: Path to check
        gitignore_spec: PathSpec object with gitignore patterns

    Returns:
        True if file is ignored, False otherwise
    """
    if gitignore_spec is None:
        return False

    try:
        # Make path relative to git_root
        relative_path = file_path.relative_to(git_root)
        # Convert to forward slashes for pathspec
        path_str = str(relative_path).replace("\\", "/")
        return gitignore_spec.match_file(path_str)
    except (ValueError, AttributeError):
        return False


def get_git_author(git_root: Path) -> Optional[str]:
    """
    Get the git user name from git config.

    Args:
        git_root: Root of the git repository

    Returns:
        Git user name, or None if not found
    """
    try:
        result = subprocess.run(
            ["git", "config", "user.name"],
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip() or None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def get_git_email(git_root: Path) -> Optional[str]:
    """
    Get the git user email from git config.

    Args:
        git_root: Root of the git repository

    Returns:
        Git user email, or None if not found
    """
    try:
        result = subprocess.run(
            ["git", "config", "user.email"],
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip() or None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def get_git_file_author(file_path: Path, git_root: Path) -> Optional[str]:
    """
    Get the author of a file from git history.

    Args:
        file_path: File to check (must be relative to git_root)
        git_root: Root of the git repository

    Returns:
        Author name, or None if not found
    """
    try:
        relative_path = file_path.relative_to(git_root)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%an", "--", str(relative_path)],
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode == 0:
            author = result.stdout.strip()
            return author if author else None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError, ValueError):
        pass
    return None


def get_git_file_date(
    file_path: Path, git_root: Path, date_format: str = "%Y-%m-%d"
) -> Optional[str]:
    """
    Get the last modified date of a file from git history.

    Args:
        file_path: File to check (must be relative to git_root)
        git_root: Root of the git repository
        date_format: Date format string (default: "%Y-%m-%d")

    Returns:
        Formatted date string, or None if not found
    """
    try:
        relative_path = file_path.relative_to(git_root)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ai", "--", str(relative_path)],
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode == 0:
            date_str = result.stdout.strip()
            if date_str:
                # Parse ISO format date and reformat
                try:
                    dt = datetime.fromisoformat(
                        date_str.replace(" ", "T").split("+")[0].split("-")[0]
                    )
                    return dt.strftime(date_format)
                except (ValueError, AttributeError):
                    # Fallback: try to extract just the date part
                    parts = date_str.split()
                    if parts:
                        return parts[0]
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError, ValueError, ImportError):
        pass
    return None


def get_git_metadata(
    file_path: Path, git_root: Path, config: Optional[Dict] = None
) -> Dict[str, Optional[str]]:
    """
    Get git metadata for a file (author, email, date).

    Args:
        file_path: File to get metadata for (must be relative to git_root)
        git_root: Root of the git repository
        config: Optional config dict with date_format

    Returns:
        Dictionary with 'author', 'email', and 'date' keys
    """
    date_format = config.get("date_format", "%Y-%m-%d") if config else "%Y-%m-%d"

    metadata = {
        "author": None,
        "email": None,
        "date": None,
    }

    # Try to get file-specific author from git history
    file_author = get_git_file_author(file_path, git_root)
    if file_author:
        metadata["author"] = file_author
    else:
        # Fallback to git config user.name
        metadata["author"] = get_git_author(git_root)

    # Get email from git config
    metadata["email"] = get_git_email(git_root)

    # Get file modification date from git
    metadata["date"] = get_git_file_date(file_path, git_root, date_format)

    return metadata
