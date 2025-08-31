# File: tests/test_newline_handling.py

"""Tests for improved newline handling."""

from pathlib import Path

import pytest

from pyannotate.annotate_headers import process_file
from tests.helpers.components import (
    WEB_FRAMEWORK_TEMPLATES,  # <- central template reuse
)
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


def test_empty_file_no_extra_newlines():
    """Test that empty files don't get unnecessary newlines."""
    empty_file = TEST_DIR / "empty.py"
    empty_file.write_text("")

    process_file(empty_file, TEST_DIR)

    processed_content = empty_file.read_text()
    expected_content = "# File: empty.py"
    assert (
        processed_content == expected_content
    ), f"Expected '{expected_content}', got '{processed_content}'"


def test_whitespace_only_file_no_extra_newlines():
    """Test that files with only whitespace are handled correctly."""
    whitespace_file = TEST_DIR / "whitespace.py"
    whitespace_file.write_text("   \n\n  \n")

    process_file(whitespace_file, TEST_DIR)

    processed_content = whitespace_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "# File: whitespace.py", "Should start with header"
    assert not processed_content.endswith("\n\n\n"), "Should not have multiple trailing newlines"


def test_single_line_file_proper_spacing():
    """Test that single-line files get proper spacing."""
    single_line_file = TEST_DIR / "single_line.py"
    original_content = "print('Hello, World!')"
    single_line_file.write_text(original_content)

    process_file(single_line_file, TEST_DIR)

    processed_content = single_line_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "# File: single_line.py", "Should start with header"
    assert lines[1] == "", "Should have blank line after header"
    assert lines[2] == "print('Hello, World!')", "Should preserve original content"
    assert len(lines) == 3, f"Should have exactly 3 lines, got {len(lines)}"


def test_multiline_file_proper_spacing():
    """Test that multi-line files get proper spacing."""
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

    assert lines[0] == "# File: multiline.py", "Should start with header"
    assert lines[1] == "", "Should have blank line after header"
    assert lines[2] == "import sys", "Should preserve original content"
    assert not processed_content.endswith("\n\n\n"), "Should not have multiple trailing newlines"


def test_shebang_file_proper_spacing():
    """Test that files with shebang get proper spacing."""
    shebang_file = TEST_DIR / "script.py"
    original_content = """#!/usr/bin/env python3
print("Hello, World!")"""
    shebang_file.write_text(original_content)

    process_file(shebang_file, TEST_DIR)

    processed_content = shebang_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "#!/usr/bin/env python3", "Should preserve shebang"
    assert lines[1] == "# File: script.py", "Should have header after shebang"
    assert lines[2] == "", "Should have blank line after header"
    assert lines[3] == 'print("Hello, World!")', "Should preserve original content"
    assert len(lines) == 4, f"Should have exactly 4 lines, got {len(lines)}"


def test_html_with_doctype_proper_spacing():
    """Test that HTML files with DOCTYPE get proper spacing."""
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

    assert lines[0] == "<!DOCTYPE html>", "Should preserve DOCTYPE"
    assert lines[1] == "<!-- File: index.html -->", "Should have header after DOCTYPE"
    assert lines[2] == "", "Should have blank line after header"
    assert lines[3] == '<html lang="en">', "Should preserve original content"


def test_xml_file_proper_spacing():
    """Test that XML files get proper spacing."""
    xml_file = TEST_DIR / "config.xml"
    original_content = """<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <setting name="debug">true</setting>
</configuration>"""
    xml_file.write_text(original_content)

    process_file(xml_file, TEST_DIR)

    processed_content = xml_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == '<?xml version="1.0" encoding="UTF-8"?>', "Should preserve XML declaration"
    assert lines[1] == "<!-- File: config.xml -->", "Should have header after declaration"
    assert lines[2] == "", "Should have blank line after header"
    assert lines[3] == "<configuration>", "Should preserve original content"


def test_vue_file_proper_spacing():
    """Test that Vue files get proper spacing."""
    vue_file = TEST_DIR / "Component.vue"
    original_content = WEB_FRAMEWORK_TEMPLATES["vue_component"]  # <- reuse, no inline duplicate
    vue_file.write_text(original_content)

    process_file(vue_file, TEST_DIR)

    processed_content = vue_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "<template>", "Should preserve template tag"
    assert lines[1] == "<!-- File: Component.vue -->", "Should have header after template"
    assert lines[2] == "", "Should have blank line after header"
    assert lines[3] == '  <div class="hello">', "Should preserve original content"


def test_existing_header_replacement_no_extra_newlines():
    """Test that replacing existing headers doesn't add extra newlines."""
    js_file = prepare_existing_header_js(TEST_DIR)

    process_file(js_file, TEST_DIR)

    processed_content = js_file.read_text()
    lines = processed_content.split("\n")

    assert lines[0] == "// File: existing_header.js", "Should have our standard header"
    assert "// Author: Someone" in processed_content, "Should preserve author info"
    assert "console.log" in processed_content, "Should preserve original content"
    assert not processed_content.endswith("\n\n\n"), "Should not have multiple trailing newlines"


def test_no_content_after_header_no_extra_newlines():
    """Test that files with only header content don't get extra newlines."""
    py_file = TEST_DIR / "header_only.py"
    original_content = "# Some comment that looks like content but isn't really"
    py_file.write_text(original_content)

    process_file(py_file, TEST_DIR)

    processed_content = py_file.read_text()

    assert processed_content.startswith("# File: header_only.py"), "Should start with header"
    assert (
        "Some comment that looks like content" in processed_content
    ), "Should preserve original comment"

    newline_count = processed_content.count("\n")
    assert newline_count <= 3, f"Should have at most 3 newlines, got {newline_count}"
