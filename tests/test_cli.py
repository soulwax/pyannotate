"""Tests for the CLI interface."""

import logging
from pathlib import Path
import tempfile
from pyannotate.cli import main, setup_logging, parse_args


def test_setup_logging(caplog):
    """Test logging configuration."""
    with caplog.at_level(logging.DEBUG):
        setup_logging(verbose=True)
        assert logging.getLogger().level == logging.DEBUG

    with caplog.at_level(logging.INFO):
        setup_logging(verbose=False)
        assert logging.getLogger().level == logging.INFO


def test_parse_args():
    """Test argument parsing."""
    args = parse_args()
    assert args.directory == Path.cwd()
    assert not args.verbose


def test_main_directory_not_found():
    """Test main function with non-existent directory."""
    with tempfile.TemporaryDirectory() as temp_path:
        nonexistent = Path(temp_path) / "nonexistent"
        exit_code = main(nonexistent)
        assert exit_code == 1


def test_main_successful_run():
    """Test main function with valid directory."""
    with tempfile.TemporaryDirectory() as temp_path:
        test_file = Path(temp_path) / "test.py"
        test_file.write_text("print('hello')")

        exit_code = main(Path(temp_path))
        assert exit_code == 0

        content = test_file.read_text()
        assert "# File: test.py" in content
