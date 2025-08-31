# File: tests/test_enhanced_headers.py

"""Tests for the enhanced header handling functionality."""

import shutil
from pathlib import Path

import pytest

from pyannotate.annotate_headers import (
    _detect_header_pattern,
    _has_existing_header,
    _merge_headers,
    _remove_existing_header,
    process_file,
)
from tests.helpers.components import (
    create_header_test_pattern_files,
    create_web_framework_test_files,
)

# Directory for temporary test files
TEST_DIR = Path("tests/enhanced_files")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True)

    # Create test files via central helpers
    create_header_test_pattern_files(TEST_DIR)
    create_web_framework_test_files(TEST_DIR)

    yield

    # Cleanup after tests
    shutil.rmtree(TEST_DIR)


def test_detect_header_pattern():
    """Test detecting existing header patterns in files."""
    patterns = create_header_test_pattern_files(TEST_DIR)

    for i, (header, expected_start, expected_end) in enumerate(patterns):
        file_path = TEST_DIR / f"pattern_{i}.txt"

        detected = _detect_header_pattern(file_path)
        assert detected is not None, f"Failed to detect pattern: {header}"
        detected_start, detected_end, _pattern = detected

        assert detected_start == expected_start, f"Incorrect start marker for {header}"
        if expected_end:
            assert detected_end == expected_end, f"Incorrect end marker for {header}"


def test_has_existing_header():
    """Test enhanced existing header detection."""
    header_formats = [
        "# File: test.py",
        "#File: test.py",  # No space
        "# file: test.py",  # Lowercase "file"
        "# Filename: test.py",
        "# @file test.py",
        "# Source: test.py",
        "# Path: test.py",
    ]

    for header in header_formats:
        assert _has_existing_header([header], "#"), f"Failed to detect header: {header}"

    # Non header content must not be detected as headers
    non_headers = [
        "# Import statements",
        "# Copyright 2023",
        "# Author: John Doe",
        "",
        "import sys",
    ]
    for non_header in non_headers:
        assert not _has_existing_header(
            [non_header], "#"
        ), f"Incorrectly detected header: {non_header}"

    # Primary header + metadata -> has to be detected
    combined_headers = [
        ["# File: test.py", "# Author: John Doe"],
        ["# Filename: test.js", "# Version: 1.0.0"],
    ]
    for header_lines in combined_headers:
        assert _has_existing_header(
            header_lines, "#"
        ), "Failed to detect valid header with metadata"


def test_remove_existing_header():
    """Test removing headers of various formats."""
    # Simple single-line header
    lines = ["# File: test.py", "", "import sys", "print('Hello')"]
    result = _remove_existing_header(lines, "#")
    assert result == ["import sys", "print('Hello')"], "Failed to remove simple header"

    # Multi-line header with comments
    lines = [
        "# File: test.py",
        "# Author: John Doe",
        "# Copyright 2023",
        "",
        "import sys",
    ]
    result = _remove_existing_header(lines, "#")
    assert result == ["import sys"], "Failed to remove multi-line header"

    # No header present
    lines = ["import sys", "print('Hello')"]
    result = _remove_existing_header(lines, "#")
    assert result == lines, "Modified content when no header exists"


def test_merge_headers():
    """Test merging existing headers with our standard format."""
    # Merge with additional information
    existing = "# File: old_path.py\n# Author: John Doe\n# Version: 1.0"
    new = "File: test.py"
    result = _merge_headers(existing, new, "#", "")

    assert "File: test.py" in result, "New file path not in merged header"
    assert "Author: John Doe" in result, "Author info not preserved"
    assert "Version: 1.0" in result, "Version info not preserved"

    # HTML-style comments
    existing = "<!-- Filename: old.html -->\n<!-- Created: 2023-07-01 -->"
    new = "File: test.html"
    result = _merge_headers(existing, new, "<!--", "-->")

    assert "File: test.html" in result, "New file path not in merged HTML header"
    assert "Created: 2023-07-01" in result, "Creation date not preserved in HTML header"


def test_web_framework_files():
    """Test processing web framework files like Vue and Svelte."""
    # Vue with <template>
    vue_file = TEST_DIR / "vue" / "Component.vue"
    process_file(vue_file, TEST_DIR)

    processed = vue_file.read_text()
    assert "<template>" in processed, "Vue template element not preserved at top"
    assert "<!-- File: vue/Component.vue -->" in processed, "Vue file header not added correctly"

    # Vue with <script setup>
    vue_setup_file = TEST_DIR / "vue" / "SetupComponent.vue"
    process_file(vue_setup_file, TEST_DIR)

    processed = vue_setup_file.read_text()
    assert "<script setup>" in processed, "Vue script setup not preserved at top"
    assert (
        "<!-- File: vue/SetupComponent.vue -->" in processed
    ), "Vue file header not added correctly"


def test_svelte_file():
    """Test processing Svelte files."""
    svelte_file = TEST_DIR / "svelte" / "Component.svelte"
    process_file(svelte_file, TEST_DIR)

    processed = svelte_file.read_text()
    assert "<script>" in processed, "Svelte script tag not preserved at top"
    assert (
        "<!-- File: svelte/Component.svelte -->" in processed
    ), "Svelte file header not added correctly"


def test_astro_file():
    """Test processing Astro files."""
    astro_file = TEST_DIR / "astro" / "Component.astro"
    process_file(astro_file, TEST_DIR)

    processed = astro_file.read_text()
    assert "---" in processed, "Astro frontmatter not preserved"
    assert (
        "<!-- File: astro/Component.astro -->" in processed
    ), "Astro file header not added correctly"


def test_react_jsx_file():
    """Test processing React JSX files."""
    react_file = TEST_DIR / "react" / "Counter.jsx"
    process_file(react_file, TEST_DIR)

    processed = react_file.read_text()
    assert processed.startswith("// File: react/Counter.jsx"), "JSX file header not added correctly"
    assert "import React" in processed, "JSX import statement not preserved"


def test_different_header_formats():
    """Test handling files with different header formats than our standard."""
    # JS file with legacy header
    js_file = TEST_DIR / "legacy" / "legacy-component.js"
    original_content = js_file.read_text()
    assert "// Version: 1.0.0" in original_content, "Test setup: Version info missing"

    process_file(js_file, TEST_DIR)
    processed = js_file.read_text()

    if not processed.startswith("// File: legacy/legacy-component.js"):
        print("\nExpected header not found. Actual content starts with:")
        print(processed[:100])

    if "// Version: 1.0.0" not in processed:
        print("\nVersion info not preserved. Header content:")
        header_lines = [line for line in processed.splitlines()[:10] if line.strip()]
        print("\n".join(header_lines))

    assert processed.startswith(
        "// File: legacy/legacy-component.js"
    ), "Header not converted to our format"
    assert "// Author: Legacy Developer" in processed, "Author information not preserved"
    assert "// Created: 2022-01-01" in processed, "Creation date not preserved"
    assert "// Version: 1.0.0" in processed, "Version info not preserved"
    assert "class LegacyComponent" in processed, "Class content preserved"
    assert "incrementCount()" in processed, "Method content preserved"

    # CSS file with deviating header
    css_file = TEST_DIR / "legacy" / "styles.css"
    process_file(css_file, TEST_DIR)

    processed = css_file.read_text()
    assert processed.startswith(
        "/* File: legacy/styles.css */"
    ), "Header not converted to our format"
    assert "Description: Main stylesheet" in processed, "Description not preserved"
    assert "Author: Design Team" in processed, "Author information not preserved"
    assert ":root {" in processed, "CSS root block preserved"
    assert "--primary-color: #4a90e2;" in processed, "CSS variables preserved"


def test_html_doctype_handling():
    """Test that HTML DOCTYPE declarations are properly preserved."""
    html_file = TEST_DIR / "html" / "index.html"
    process_file(html_file, TEST_DIR)

    processed = html_file.read_text()
    lines = processed.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]

    assert "<!DOCTYPE html>" in non_empty_lines[0], "DOCTYPE not preserved at the first line"
    assert "<!-- File: html/index.html -->" in non_empty_lines[1], "Header not placed after DOCTYPE"
    assert '<html lang="en">' in processed, "HTML element not preserved"
    assert "<title>Sample Page</title>" in processed, "Title not preserved"


def test_skipped_file_types():
    """Test that specific file types are skipped."""
    md_file = TEST_DIR / "README.md"
    json_file = TEST_DIR / "config.json"
    md_content = """# Project Title
A simple project description.
Installation
Installation instructions here.
"""
    json_content = """{
"name": "test-project",
"version": "1.0.0",
"description": "A test project"
}"""
    md_file.write_text(md_content)
    json_file.write_text(json_content)

    process_file(md_file, TEST_DIR)
    process_file(json_file, TEST_DIR)

    assert md_file.read_text() == md_content, "Markdown file was modified but should be skipped"
    assert json_file.read_text() == json_content, "JSON file was modified but should be skipped"
