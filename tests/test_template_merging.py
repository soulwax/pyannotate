# File: tests/test_template_merging.py

"""Tests for template merging with existing headers."""

import json
import tempfile
from pathlib import Path

from annot8.annotate_headers import process_file
from annot8.config import load_config


class TestTemplateMerging:
    """Test that multi-line templates are preserved when merging with existing headers."""

    def test_multi_line_template_preserved_with_existing_header(self):
        """Test that multi-line templates are not truncated when file has existing header."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".annot8.json"
            config_data = {
                "header": {
                    "template": (
                        "File: {file_path}\nAuthor: {author|Unknown}\n" "Version: {version|1.0.0}"
                    )
                }
            }
            config_file.write_text(json.dumps(config_data))

            # Create file with existing header
            test_file = temp_path / "test.py"
            test_file.write_text("# File: test.py\n# Old comment\nprint('hello')")

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            # All template lines should be present
            assert "# File: test.py" in content
            assert "# Author: Unknown" in content
            assert "# Version: 1.0.0" in content
            # Old comment should be removed
            assert "Old comment" not in content
            # Code should be preserved
            assert "print('hello')" in content

    def test_single_line_header_merges_correctly(self):
        """Test that single-line headers still merge correctly (backward compatibility)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # No template - uses default single-line format
            test_file = temp_path / "test.py"
            test_file.write_text("# File: test.py\n# Author: Old Author\nprint('hello')")

            # Process without template (default behavior)
            process_file(test_file, temp_path)

            content = test_file.read_text()
            # File path should be updated
            assert "# File: test.py" in content
            # Old author metadata should be preserved
            assert "# Author: Old Author" in content
            assert "print('hello')" in content

    def test_multi_line_template_with_metadata_preserved(self):
        """Test multi-line template with metadata from existing header."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".annot8.json"
            config_data = {
                "header": {
                    "template": (
                        "File: {file_path}\n"
                        "Author: {author|Unknown}\n"
                        "Date: {date}\n"
                        "Description: Custom template"
                    ),
                    "include_date": True,
                }
            }
            config_file.write_text(json.dumps(config_data))

            # Create file with existing header that has metadata
            test_file = temp_path / "test.py"
            test_file.write_text(
                "# File: test.py\n# Copyright: 2024\n# License: MIT\nprint('hello')"
            )

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            # All template lines should be present
            assert "# File: test.py" in content
            assert "# Author: Unknown" in content
            assert "# Date:" in content
            assert "# Description: Custom template" in content
            # Template should replace old header entirely
            assert "Copyright: 2024" not in content
            assert "License: MIT" not in content
            assert "print('hello')" in content
