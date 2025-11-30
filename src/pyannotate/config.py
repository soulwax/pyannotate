# File: src/pyannotate/config.py

"""Configuration file loading and management for PyAnnotate."""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Set

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # type: ignore
    except ImportError:
        tomllib = None  # type: ignore

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


@dataclass
class HeaderConfig:
    """Configuration for header metadata and templates."""

    # Metadata fields
    author: Optional[str] = None
    author_email: Optional[str] = None
    version: Optional[str] = None
    include_date: bool = False
    date_format: str = "%Y-%m-%d"

    # Template customization
    template: Optional[str] = None  # Custom header template with variables


@dataclass
class FileConfig:
    """Configuration for file processing."""

    # Additional ignored files and directories
    ignored_files: Set[str] = field(default_factory=set)
    ignored_directories: Set[str] = field(default_factory=set)

    # Custom file patterns (extension -> comment style)
    custom_patterns: Dict[str, Dict[str, str]] = field(default_factory=dict)


@dataclass
class PyAnnotateConfig:
    """Main configuration class for PyAnnotate."""

    header: HeaderConfig = field(default_factory=HeaderConfig)
    files: FileConfig = field(default_factory=FileConfig)

    @classmethod
    def default(cls) -> "PyAnnotateConfig":
        """Create a default configuration."""
        return cls()


def _find_config_file(directory: Path) -> Optional[Path]:
    """
    Find configuration file in the given directory or parent directories.

    Looks for:
    - .pyannotate.yaml
    - .pyannotate.yml
    - .pyannotate.json
    - pyproject.toml (with [tool.pyannotate] section)

    Args:
        directory: Directory to search from (searches upward)

    Returns:
        Path to config file if found, None otherwise
    """
    current = directory.resolve()

    # Search upward from current directory
    while current != current.parent:
        # Check for dedicated config files
        for filename in [".pyannotate.yaml", ".pyannotate.yml", ".pyannotate.json"]:
            config_path = current / filename
            if config_path.is_file():
                return config_path

        # Check for pyproject.toml
        pyproject_path = current / "pyproject.toml"
        if pyproject_path.is_file():
            return pyproject_path

        current = current.parent

    return None


def _load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if yaml is None:
        logging.warning(
            "YAML config file found but 'pyyaml' is not installed. "
            "Install it with: pip install pyyaml"
        )
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError) as e:  # type: ignore
        logging.warning("Failed to load YAML config from %s: %s", config_path, e)
        return {}


def _load_json_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except (OSError, json.JSONDecodeError) as e:
        logging.warning("Failed to load JSON config from %s: %s", config_path, e)
        return {}


def _load_toml_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from TOML file (pyproject.toml)."""
    if tomllib is None:
        logging.warning(
            "TOML config file found but 'tomli' is not installed (Python < 3.11). "
            "Install it with: pip install tomli"
        )
        return {}

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
            # Extract [tool.pyannotate] section
            return data.get("tool", {}).get("pyannotate", {})
    except OSError as e:
        logging.warning("Failed to load TOML config from %s: %s", config_path, e)
        return {}
    except (ValueError, KeyError) as e:
        # TOML parsing errors or missing sections
        logging.warning("Failed to parse TOML config from %s: %s", config_path, e)
        return {}


def _load_config_file(config_path: Path) -> Dict[str, Any]:
    """
    Load configuration from a file based on its extension.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary with configuration data
    """
    suffix = config_path.suffix.lower()

    if suffix in {".yaml", ".yml"}:
        return _load_yaml_config(config_path)
    if suffix == ".json":
        return _load_json_config(config_path)
    if suffix == ".toml" or config_path.name == "pyproject.toml":
        return _load_toml_config(config_path)
    logging.warning("Unsupported config file format: %s", config_path)
    return {}


def _parse_config_dict(config_data: Dict[str, Any]) -> PyAnnotateConfig:
    """
    Parse configuration dictionary into PyAnnotateConfig object.

    Args:
        config_data: Raw configuration dictionary

    Returns:
        Parsed configuration object
    """
    config = PyAnnotateConfig()

    # Parse header configuration
    if "header" in config_data:
        header_data = config_data["header"]
        if isinstance(header_data, dict):
            config.header = HeaderConfig(
                author=header_data.get("author"),
                author_email=header_data.get("author_email"),
                version=header_data.get("version"),
                include_date=header_data.get("include_date", False),
                date_format=header_data.get("date_format", "%Y-%m-%d"),
                template=header_data.get("template"),
            )

    # Parse file configuration
    if "files" in config_data:
        files_data = config_data["files"]
        if isinstance(files_data, dict):
            config.files = FileConfig(
                ignored_files=set(files_data.get("ignored_files", [])),
                ignored_directories=set(files_data.get("ignored_directories", [])),
                custom_patterns=files_data.get("custom_patterns", {}),
            )

    return config


def load_config(project_root: Path) -> PyAnnotateConfig:
    """
    Load configuration from file if it exists, otherwise return default config.

    Args:
        project_root: Root directory of the project to search for config

    Returns:
        PyAnnotateConfig object with loaded or default settings
    """
    config_path = _find_config_file(project_root)

    if config_path is None:
        logging.debug("No configuration file found, using defaults")
        return PyAnnotateConfig.default()

    logging.info("Loading configuration from: %s", config_path)
    config_data = _load_config_file(config_path)

    if not config_data:
        logging.debug("Configuration file is empty, using defaults")
        return PyAnnotateConfig.default()

    try:
        return _parse_config_dict(config_data)
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        logging.warning("Error parsing configuration: %s. Using defaults.", e)
        return PyAnnotateConfig.default()
