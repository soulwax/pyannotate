# File: tests/test_newline_handling.py

"""Tests for improved newline handling (relaxed: no strict trailing-newline limits)."""

from pathlib import Path

import pytest

from annot8.annotate_headers import process_file
from tests.helpers.components import WEB_FRAMEWORK_TEMPLATES
from tests.test_utils import (
    cleanup_test_directory,
    create_temp_test_directory,
    prepare_existing_header_js,
)

# Directory for temporary test files
TEST_DIR = Path("tests/newline_test")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    create_temp_test_directory(TEST_DIR)
    yield
    cleanup_test_directory(TEST_DIR)


def test_empty_file_header_added():
    """Empty files should just get the header (with trailing newline)."""
    empty_file = TEST_DIR / "empty.py"
    empty_file.write_text("")

    process_file(empty_file, TEST_DIR)

    processed_content = empty_file.read_text()
    expected_content = "# File: empty.py\n"  # trailing newline is now expected
    assert processed_content == expected_content


def test_whitespace_only_file_header_added():
    """Whitespace-only files should get the header without strict trailing-newline checks."""
    whitespace_file = TEST_DIR / "whitespace.py"
    whitespace_file.write_text("   \n\n  \n")

    process_file(whitespace_file, TEST_DIR)

    processed_content = whitespace_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "# File: whitespace.py"


def test_single_line_file_proper_spacing():
    """Single-line files get a blank line after the header (no strict trailing-newline checks)."""
    single_line_file = TEST_DIR / "single_line.py"
    original_content = "print('Hello, World!')"
    single_line_file.write_text(original_content)

    process_file(single_line_file, TEST_DIR)

    processed_content = single_line_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "# File: single_line.py"
    assert lines[1] == ""
    assert lines[2] == "print('Hello, World!')"


def test_multiline_file_proper_spacing():
    """Multi-line files get a blank line after the header (no strict trailing-newline checks)."""
    multiline_file = TEST_DIR / "multiline.py"
    original_content = """import sys
import os

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()"""
    multiline_file.write_text(original_content)

    process_file(multiline_file, TEST_DIR)

    processed_content = multiline_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "# File: multiline.py"
    assert lines[1] == ""
    assert lines[2] == "import sys"


def test_shebang_file_proper_spacing():
    """Files with shebang keep shebang, then header, then content."""
    shebang_file = TEST_DIR / "script.py"
    original_content = """#!/usr/bin/env python3
print("Hello, World!")"""
    shebang_file.write_text(original_content)

    process_file(shebang_file, TEST_DIR)

    processed_content = shebang_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "#!/usr/bin/env python3"
    assert lines[1] == "# File: script.py"
    assert lines[2] == ""
    assert lines[3] == 'print("Hello, World!")'


def test_html_with_doctype_proper_spacing():
    """HTML files with DOCTYPE keep DOCTYPE, then header."""
    html_file = TEST_DIR / "index.html"
    original_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Test</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>"""
    html_file.write_text(original_content)

    process_file(html_file, TEST_DIR)

    processed_content = html_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "<!DOCTYPE html>"
    assert lines[1] == "<!-- File: index.html -->"
    assert lines[2] == ""
    assert lines[3] == '<html lang="en">'


def test_xml_file_proper_spacing():
    """XML files keep XML declaration, then header."""
    xml_file = TEST_DIR / "config.xml"
    original_content = """<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <setting name="debug">true</setting>
</configuration>"""
    xml_file.write_text(original_content)

    process_file(xml_file, TEST_DIR)

    processed_content = xml_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == '<?xml version="1.0" encoding="UTF-8"?>'
    assert lines[1] == "<!-- File: config.xml -->"
    assert lines[2] == ""
    assert lines[3] == "<configuration>"


def test_vue_file_proper_spacing():
    """Vue files keep <template> first, then header."""
    vue_file = TEST_DIR / "Component.vue"
    original_content = WEB_FRAMEWORK_TEMPLATES["vue_component"]
    vue_file.write_text(original_content)

    process_file(vue_file, TEST_DIR)

    processed_content = vue_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "<template>"
    assert lines[1] == "<!-- File: Component.vue -->"
    assert lines[2] == ""
    assert lines[3] == '  <div class="hello">'


def test_existing_header_replacement_structure():
    """Existing legacy headers should be merged with our format (no strict newline checks)."""
    js_file = prepare_existing_header_js(TEST_DIR)

    process_file(js_file, TEST_DIR)

    processed_content = js_file.read_text()

    assert processed_content.split("\n")[0] == "// File: existing_header.js"
    assert "// Author: Someone" in processed_content
    assert "console.log" in processed_content


def test_comment_only_file_header_added():
    """Comment-only files should keep comment content and add header (no strict newline checks)."""
    py_file = TEST_DIR / "header_only.py"
    original_content = "# Some comment that looks like content but isn't really"
    py_file.write_text(original_content)

    process_file(py_file, TEST_DIR)

    processed_content = py_file.read_text()

    assert processed_content.startswith("# File: header_only.py")
    assert "Some comment that looks like content" in processed_content
