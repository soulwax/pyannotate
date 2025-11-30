# File: tests/test_config.py
# pylint: disable=duplicate-code

"""Tests for configuration file loading."""

import json
import tempfile
from pathlib import Path

from pyannotate.config import (
    HeaderConfig,
    FileConfig,
    PyAnnotateConfig,
    load_config,
    _find_config_file,
    _load_json_config,
    _parse_config_dict,
)


class TestConfigDataClasses:
    """Test configuration data classes."""

    def test_default_config(self):
        """Test default configuration creation."""
        config = PyAnnotateConfig.default()
        assert isinstance(config.header, HeaderConfig)
        assert isinstance(config.files, FileConfig)
        assert config.header.author is None
        assert config.header.include_date is False
        assert len(config.files.ignored_files) == 0
        assert len(config.files.ignored_directories) == 0

    def test_header_config(self):
        """Test HeaderConfig creation."""
        header = HeaderConfig(
            author="Test Author",
            author_email="test@example.com",
            version="1.0.0",
            include_date=True,
        )
        assert header.author == "Test Author"
        assert header.author_email == "test@example.com"
        assert header.version == "1.0.0"
        assert header.include_date is True

    def test_file_config(self):
        """Test FileConfig creation."""
        files = FileConfig(
            ignored_files={"custom.txt", "test.ignore"},
            ignored_directories={"custom_dir"},
        )
        assert "custom.txt" in files.ignored_files
        assert "custom_dir" in files.ignored_directories


class TestConfigFileLoading:
    """Test configuration file loading."""

    def test_find_config_file_yaml(self):
        """Test finding YAML config file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.yaml"
            config_file.write_text("header:\n  author: Test\n")

            found = _find_config_file(temp_path)
            assert found == config_file

    def test_find_config_file_json(self):
        """Test finding JSON config file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_file.write_text('{"header": {"author": "Test"}}')

            found = _find_config_file(temp_path)
            assert found == config_file

    def test_find_config_file_none(self):
        """Test when no config file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            found = _find_config_file(temp_path)
            assert found is None

    def test_load_json_config(self):
        """Test loading JSON configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {
                "header": {
                    "author": "Test Author",
                    "author_email": "test@example.com",
                    "include_date": True,
                },
                "files": {
                    "ignored_files": ["custom.txt"],
                    "ignored_directories": ["custom_dir"],
                },
            }
            config_file.write_text(json.dumps(config_data))

            loaded = _load_json_config(config_file)
            assert loaded == config_data

    def test_parse_config_dict(self):
        """Test parsing configuration dictionary."""
        config_data = {
            "header": {
                "author": "Test Author",
                "author_email": "test@example.com",
                "version": "1.0.0",
                "include_date": True,
                "date_format": "%Y-%m-%d",
            },
            "files": {
                "ignored_files": ["custom.txt", "test.ignore"],
                "ignored_directories": ["custom_dir"],
            },
        }

        config = _parse_config_dict(config_data)

        assert config.header.author == "Test Author"
        assert config.header.author_email == "test@example.com"
        assert config.header.version == "1.0.0"
        assert config.header.include_date is True
        assert "custom.txt" in config.files.ignored_files
        assert "custom_dir" in config.files.ignored_directories

    def test_load_config_with_file(self):
        """Test loading configuration from file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {
                "header": {"author": "Test Author"},
                "files": {"ignored_files": ["test.ignore"]},
            }
            config_file.write_text(json.dumps(config_data))

            config = load_config(temp_path)
            assert config.header.author == "Test Author"
            assert "test.ignore" in config.files.ignored_files

    def test_load_config_no_file(self):
        """Test loading configuration when no file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config = load_config(temp_path)
            # Should return default config
            assert config.header.author is None
            assert len(config.files.ignored_files) == 0

    def test_load_config_empty_file(self):
        """Test loading configuration from empty file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_file.write_text("{}")

            config = load_config(temp_path)
            # Should return default config when file is empty
            assert config.header.author is None

    def test_load_config_partial(self):
        """Test loading configuration with partial data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_file.write_text('{"header": {"author": "Test"}}')

            config = load_config(temp_path)
            assert config.header.author == "Test"
            # Files config should be default
            assert len(config.files.ignored_files) == 0
