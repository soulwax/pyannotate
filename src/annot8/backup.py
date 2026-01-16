# File: src/annot8/backup.py

"""Backup and revert functionality for Annot8."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

BACKUP_FILENAME = ".annot8_backup.json"


def _get_backup_path(project_root: Path) -> Path:
    """Get the path to the backup file."""
    return project_root / BACKUP_FILENAME


def save_backup(project_root: Path, file_backups: Dict[str, str]) -> None:
    """
    Save file backups to the backup file.

    Args:
        project_root: Root directory of the project
        file_backups: Dictionary mapping relative file paths to their original content
    """
    if not file_backups:
        logging.debug("No files to backup")
        return

    backup_path = _get_backup_path(project_root)
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "files": file_backups,
    }

    try:
        backup_path.write_text(json.dumps(backup_data, indent=2), encoding="utf-8")
        logging.debug("Saved backup for %d files to %s", len(file_backups), backup_path)
    except (OSError, ValueError, TypeError) as e:
        logging.warning("Failed to save backup: %s", e)


def load_backup(project_root: Path) -> Optional[Dict[str, str]]:
    """
    Load the most recent backup from the backup file.

    Args:
        project_root: Root directory of the project

    Returns:
        Dictionary mapping relative file paths to their original content,
        or None if no backup exists
    """
    backup_path = _get_backup_path(project_root)
    if not backup_path.exists():
        logging.debug("No backup file found at %s", backup_path)
        return None

    try:
        backup_data = json.loads(backup_path.read_text(encoding="utf-8"))
        files = backup_data.get("files", {})
        timestamp = backup_data.get("timestamp", "unknown")
        logging.debug(
            "Loaded backup from %s (timestamp: %s, %d files)", backup_path, timestamp, len(files)
        )
        return files
    except (OSError, json.JSONDecodeError) as e:
        logging.warning("Failed to load backup: %s", e)
        return None


def revert_files(project_root: Path, dry_run: bool = False) -> Dict[str, int]:
    """
    Revert files from the most recent backup.

    Args:
        project_root: Root directory of the project
        dry_run: If True, preview changes without modifying files

    Returns:
        Dictionary with statistics: {"reverted": int, "missing": int, "errors": int}
    """
    file_backups = load_backup(project_root)
    if not file_backups:
        logging.warning("No backup found to revert from")
        return {"reverted": 0, "missing": 0, "errors": 0}

    stats = {"reverted": 0, "missing": 0, "errors": 0}

    for relative_path, original_content in file_backups.items():
        file_path = project_root / relative_path

        if not file_path.exists():
            logging.warning("File no longer exists, cannot revert: %s", file_path)
            stats["missing"] += 1
            continue

        try:
            if dry_run:
                logging.info("[DRY-RUN] Would revert: %s", file_path)
            else:
                file_path.write_text(original_content, encoding="utf-8")
                logging.info("Reverted: %s", file_path)
            stats["reverted"] += 1
        except (OSError, UnicodeEncodeError) as e:
            logging.error("Failed to revert %s: %s", file_path, e)
            stats["errors"] += 1

    if not dry_run and stats["reverted"] > 0:
        # Optionally remove backup file after successful revert
        # For now, we'll keep it in case user wants to revert again
        logging.debug("Revert complete. Backup file kept at %s", _get_backup_path(project_root))

    return stats


def clear_backup(project_root: Path) -> bool:
    """
    Clear the backup file.

    Args:
        project_root: Root directory of the project

    Returns:
        True if backup was cleared, False if it didn't exist
    """
    backup_path = _get_backup_path(project_root)
    if backup_path.exists():
        try:
            backup_path.unlink()
            logging.debug("Cleared backup file: %s", backup_path)
            return True
        except OSError as e:
            logging.warning("Failed to clear backup file: %s", e)
            return False
    return False
