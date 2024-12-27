"""Tests for the CLI interface."""

import logging
from pathlib import Path

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
    # Test default arguments
    args = parse_args()
    assert args.directory == Path.cwd()
    assert not args.verbose


def test_main_directory_not_found(tmp_path):
    """Test main function with non-existent directory."""
    nonexistent = tmp_path / "nonexistent"
    exit_code = main(nonexistent)
    assert exit_code == 1


def test_main_successful_run(tmp_path):
    """Test main function with valid directory."""
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")

    exit_code = main(tmp_path)
    assert exit_code == 0

    content = test_file.read_text()
    assert "# File: test.py" in content
