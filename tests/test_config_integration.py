# File: tests/test_config_integration.py

"""Integration tests for configuration file usage."""

import json
import tempfile
from pathlib import Path

from annot8.annotate_headers import process_file, walk_directory
from annot8.config import load_config


class TestConfigIntegration:
    """Test configuration integration with file processing."""

    def test_config_ignored_files(self):
        """Test that config-ignored files are actually skipped."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create config file
            config_file = temp_path / ".annot8.json"
            config_data = {"files": {"ignored_files": ["custom_ignore.txt"]}}
            config_file.write_text(json.dumps(config_data))

            # Create test files
            normal_file = temp_path / "normal.py"
            ignored_file = temp_path / "custom_ignore.txt"
            normal_file.write_text("print('test')")
            ignored_file.write_text("This should be ignored")

            # Load config
            config = load_config(temp_path)

            # Process files
            normal_result = process_file(normal_file, temp_path, config=config)
            ignored_result = process_file(ignored_file, temp_path, config=config)

            # Normal file should be processed
            assert normal_result["status"] == "modified"
            assert "# File:" in normal_file.read_text()

            # Ignored file should be skipped
            assert ignored_result["status"] == "skipped"
            assert "This should be ignored" in ignored_file.read_text()
            assert "# File:" not in ignored_file.read_text()

    def test_config_ignored_directories(self):
        """Test that config-ignored directories are skipped."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create config file
            config_file = temp_path / ".annot8.json"
            config_data = {"files": {"ignored_directories": ["skip_me"]}}
            config_file.write_text(json.dumps(config_data))

            # Create directory structure
            skip_dir = temp_path / "skip_me"
            skip_dir.mkdir()
            skip_file = skip_dir / "test.py"
            skip_file.write_text("print('test')")

            normal_dir = temp_path / "normal"
            normal_dir.mkdir()
            normal_file = normal_dir / "test.py"
            normal_file.write_text("print('test')")

            # Load config
            config = load_config(temp_path)

            # Process directory
            stats = walk_directory(temp_path, temp_path, config=config)

            # Normal file should be processed
            assert "# File:" in normal_file.read_text()

            # Skipped file should not be processed
            assert "print('test')" in skip_file.read_text()
            assert "# File:" not in skip_file.read_text()

            # Stats should reflect skipped files
            assert stats["skipped"] >= 1

    def test_config_without_file(self):
        """Test that processing works without config file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            test_file = temp_path / "test.py"
            test_file.write_text("print('test')")

            # Process without config (should use defaults)
            result = process_file(test_file, temp_path)

            assert result["status"] == "modified"
            assert "# File:" in test_file.read_text()
