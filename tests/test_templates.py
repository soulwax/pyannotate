# File: tests/test_templates.py
# pylint: disable=duplicate-code

"""Tests for custom header templates."""

import json
import re
import tempfile
from pathlib import Path

from pyannotate.annotate_headers import process_file
from pyannotate.config import load_config


class TestTemplateRendering:
    """Test template rendering functionality."""

    def test_simple_template(self):
        """Test simple template with file_path variable."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {"header": {"template": "File: {file_path}"}}
            config_file.write_text(json.dumps(config_data))

            test_file = temp_path / "test.py"
            test_file.write_text("print('hello')")

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            assert "# File: test.py" in content

    def test_multi_line_template(self):
        """Test multi-line template."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {
                "header": {"template": "File: {file_path}\nAuthor: {author|Unknown}\nDate: {date}"}
            }
            config_file.write_text(json.dumps(config_data))

            test_file = temp_path / "test.py"
            test_file.write_text("print('hello')")

            config = load_config(temp_path)
            config.header.include_date = True
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            assert "# File: test.py" in content
            assert "# Author: Unknown" in content
            assert "# Date:" in content

    def test_template_with_author(self):
        """Test template with author variable."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {
                "header": {"author": "John Doe", "template": "File: {file_path}\nAuthor: {author}"}
            }
            config_file.write_text(json.dumps(config_data))

            test_file = temp_path / "test.py"
            test_file.write_text("print('hello')")

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            assert "# File: test.py" in content
            assert "# Author: John Doe" in content

    def test_template_with_defaults(self):
        """Test template with default values for missing variables."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {
                "header": {
                    "template": (
                        "File: {file_path}\nVersion: {version|1.0.0}\n" "Author: {author|Anonymous}"
                    )
                }
            }
            config_file.write_text(json.dumps(config_data))

            test_file = temp_path / "test.py"
            test_file.write_text("print('hello')")

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            assert "# File: test.py" in content
            assert "# Version: 1.0.0" in content
            assert "# Author: Anonymous" in content

    def test_template_with_date(self):
        """Test template with date variable."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {
                "header": {
                    "include_date": True,
                    "date_format": "%Y-%m-%d",
                    "template": "File: {file_path}\nCreated: {date}",
                }
            }
            config_file.write_text(json.dumps(config_data))

            test_file = temp_path / "test.py"
            test_file.write_text("print('hello')")

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            assert "# File: test.py" in content
            assert "# Created:" in content
            # Date should be in YYYY-MM-DD format
            assert re.search(r"# Created: \d{4}-\d{2}-\d{2}", content)

    def test_template_file_variables(self):
        """Test template with file-specific variables."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            sub_dir = temp_path / "src" / "utils"
            sub_dir.mkdir(parents=True)

            config_file = temp_path / ".pyannotate.json"
            config_data = {
                "header": {
                    "template": (
                        "File: {file_path}\nName: {file_name}\nStem: {file_stem}\n"
                        "Suffix: {file_suffix}\nDir: {file_dir}"
                    )
                }
            }
            config_file.write_text(json.dumps(config_data))

            test_file = sub_dir / "helper.py"
            test_file.write_text("def help(): pass")

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            assert "# File: src/utils/helper.py" in content
            assert "# Name: helper.py" in content
            assert "# Stem: helper" in content
            assert "# Suffix: .py" in content
            assert "# Dir: src/utils" in content

    def test_template_empty_lines(self):
        """Test template with empty lines for spacing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {
                "header": {"template": "File: {file_path}\n\nDescription: This is a test file"}
            }
            config_file.write_text(json.dumps(config_data))

            test_file = temp_path / "test.py"
            test_file.write_text("print('hello')")

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            lines = content.splitlines()
            # Should have empty line between file_path and description
            file_line_idx = next(i for i, line in enumerate(lines) if "File: test.py" in line)
            desc_line_idx = next(i for i, line in enumerate(lines) if "Description:" in line)
            assert desc_line_idx == file_line_idx + 2  # One empty line between

    def test_template_with_css_comments(self):
        """Test template with CSS-style comments."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_file = temp_path / ".pyannotate.json"
            config_data = {"header": {"template": "File: {file_path}\nAuthor: {author|Unknown}"}}
            config_file.write_text(json.dumps(config_data))

            test_file = temp_path / "test.css"
            test_file.write_text("body { margin: 0; }")

            config = load_config(temp_path)
            process_file(test_file, temp_path, config=config)

            content = test_file.read_text()
            assert "/* File: test.css */" in content
            assert "/* Author: Unknown */" in content

    def test_template_without_config(self):
        """Test that default behavior works without template."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            test_file = temp_path / "test.py"
            test_file.write_text("print('hello')")

            # Process without config (should use default)
            process_file(test_file, temp_path)

            content = test_file.read_text()
            assert "# File: test.py" in content
            # Should not have author/date unless configured
            assert "Author:" not in content
