# File: tests/test_enhanced_headers.py

"""Tests for the enhanced header handling functionality."""

import os
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

# Directory for temporary test files
TEST_DIR = Path("tests/enhanced_files")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True)

    # Create test directories
    web_dir = TEST_DIR / "web"
    web_dir.mkdir()

    # Create sample files with different header patterns
    _create_test_pattern_files()
    _create_web_framework_test_files()

    yield

    # Cleanup after tests
    shutil.rmtree(TEST_DIR)


def _create_test_pattern_files():
    """Create test files with different header patterns."""
    patterns = [
        ("# File: test.py", "#", ""),
        ("// Filename: test.js", "//", ""),
        ("/* Source: test.css */", "/*", "*/"),
        ("<!-- Path: test.html -->", "<!--", "-->"),
        ("# @file test.rb", "#", ""),
    ]

    for i, (header, comment_start, comment_end) in enumerate(patterns):
        file_path = TEST_DIR / f"pattern_{i}.txt"
        content = f"{header}\nprint('test')\n"
        file_path.write_text(content)


def _create_web_framework_test_files():
    """Create test files for web frameworks."""
    # Basic Vue component
    vue_component = """<template>
      <div class="hello">
        <h1>{{ msg }}</h1>
        <p>
          Welcome to your Vue.js application
        </p>
      </div>
    </template>

    <script>
    export default {
      name: 'HelloWorld',
      props: {
        msg: String
      }
    }
    </script>

    <style scoped>
    h1 {
      margin: 40px 0 0;
      color: #42b983;
    }
    </style>
    """

    # Vue with script setup
    vue_setup = """<script setup>
    import { ref, onMounted } from 'vue'

    const count = ref(0)
    const message = ref('Hello Vue 3!')

    onMounted(() => {
      console.log('Component mounted')
    })
    </script>

    <template>
      <div class="container">
        <h1>{{ message }}</h1>
        <button @click="count++">Count: {{ count }}</button>
      </div>
    </template>

    <style scoped>
    .container {
      text-align: center;
      margin-top: 60px;
    }
    </style>
    """

    # Svelte component
    svelte_component = """<script>
      export let name = 'world';
      let count = 0;
      
      function handleClick() {
        count += 1;
      }
    </script>

    <main>
      <h1>Hello {name}!</h1>
      <button on:click={handleClick}>
        Clicked {count} {count === 1 ? 'time' : 'times'}
      </button>
    </main>

    <style>
      main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
      }
      
      h1 {
        color: #ff3e00;
        font-size: 4em;
        font-weight: 100;
      }
      
      button {
        background-color: #ff3e00;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 4px;
      }
    </style>
    """

    # Astro component
    astro_component = """---
    // Component imports and props
    import { Button } from '../components/Button.astro';
    const { title = 'Default Title' } = Astro.props;
    ---

    <section class="hero">
      <h1>{title}</h1>
      <p>Welcome to my Astro site!</p>
      <Button text="Learn more" />
    </section>

    <style>
      .hero {
        padding: 4rem;
        text-align: center;
      }
      h1 {
        font-size: 3rem;
        font-weight: 800;
      }
    </style>

    <script>
      // Client-side JavaScript
      document.querySelector('h1').addEventListener('click', () => {
        alert('Hello from Astro!');
      });
    </script>
    """

    # React JSX component
    react_component = """import React, { useState, useEffect } from 'react';

    function Counter() {
      const [count, setCount] = useState(0);
      
      useEffect(() => {
        document.title = `You clicked ${count} times`;
      }, [count]);
      
      return (
        <div className="counter">
          <h1>You clicked {count} times</h1>
          <button onClick={() => setCount(count + 1)}>
            Click me
          </button>
        </div>
      );
    }

    export default Counter;
    """

    # HTML file with doctype
    html_file = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sample Page</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header>
            <h1>Welcome to our website</h1>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </header>

        <main>
            <section>
                <h2>Main Content</h2>
                <p>This is a sample HTML page for testing the PyAnnotate tool.</p>
            </section>
        </main>

        <footer>
            <p>&copy; 2025 PyAnnotate Example</p>
        </footer>

        <script src="main.js"></script>
    </body>
    </html>
    """

    # File with different header format
    different_header_js = """// Filename: legacy-component.js
    // Author: Legacy Developer
    // Created: 2022-01-01
    // Version: 1.0.0

    class LegacyComponent {
      constructor(props) {
        this.props = props;
        this.state = {
          count: 0
        };
      }
      
      incrementCount() {
        this.state.count++;
        console.log(`Count is now ${this.state.count}`);
      }
      
      render() {
        return `<div class="legacy-component">
          <h2>${this.props.title}</h2>
          <p>Count: ${this.state.count}</p>
          <button onClick="this.incrementCount()">Increment</button>
        </div>`;
      }
    }

    export default LegacyComponent;
    """

    # CSS with header using different format
    css_with_header = """/* Source: styles.css
     * Description: Main stylesheet for the application
     * Author: Design Team
     */

    :root {
      --primary-color: #4a90e2;
      --secondary-color: #e74c3c;
      --text-color: #333;
      --background-color: #f9f9f9;
    }

    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      color: var(--text-color);
      background-color: var(--background-color);
      margin: 0;
      padding: 0;
    }
    """

    # Create subdirectories
    web_dirs = ["vue", "svelte", "astro", "react", "html", "legacy"]
    for dir_name in web_dirs:
        os.makedirs(TEST_DIR / dir_name, exist_ok=True)

    # Write test files
    (TEST_DIR / "vue" / "Component.vue").write_text(vue_component)
    (TEST_DIR / "vue" / "SetupComponent.vue").write_text(vue_setup)
    (TEST_DIR / "svelte" / "Component.svelte").write_text(svelte_component)
    (TEST_DIR / "astro" / "Component.astro").write_text(astro_component)
    (TEST_DIR / "react" / "Counter.jsx").write_text(react_component)
    (TEST_DIR / "html" / "index.html").write_text(html_file)
    (TEST_DIR / "legacy" / "legacy-component.js").write_text(different_header_js)
    (TEST_DIR / "legacy" / "styles.css").write_text(css_with_header)


def test_detect_header_pattern():
    """Test detecting existing header patterns in files."""
    patterns = [
        ("# File: test.py", "#", ""),
        ("// Filename: test.js", "//", ""),
        ("/* Source: test.css */", "/*", "*/"),
        ("<!-- Path: test.html -->", "<!--", "-->"),
        ("# @file test.rb", "#", ""),
    ]

    for i, (header, expected_start, expected_end) in enumerate(patterns):
        file_path = TEST_DIR / f"pattern_{i}.txt"

        # Test detection
        detected = _detect_header_pattern(file_path)
        assert detected is not None, f"Failed to detect pattern: {header}"
        detected_start, detected_end, pattern = detected

        # We only check if the comment markers are correctly detected
        assert detected_start == expected_start, f"Incorrect start marker for {header}"
        if expected_end:  # Only check end marker if it exists
            assert detected_end == expected_end, f"Incorrect end marker for {header}"


def test_has_existing_header():
    """Test enhanced existing header detection."""
    # Test various header formats
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
        # Check if our function can detect each format
        assert _has_existing_header([header], "#"), f"Failed to detect header: {header}"

    # Test non-header content - these should not be detected as headers
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

    # But a file with the primary header and metadata should be detected
    combined_headers = [
        ["# File: test.py", "# Author: John Doe"],
        ["# Filename: test.js", "# Version: 1.0.0"],
    ]

    for header_lines in combined_headers:
        assert _has_existing_header(
            header_lines, "#"
        ), f"Failed to detect valid header with metadata"


def test_remove_existing_header():
    """Test removing headers of various formats."""
    # Test single-line header
    lines = ["# File: test.py", "", "import sys", "print('Hello')"]
    result = _remove_existing_header(lines, "#")
    assert result == ["import sys", "print('Hello')"], "Failed to remove simple header"

    # Test multi-line header with comments
    lines = [
        "# File: test.py",
        "# Author: John Doe",
        "# Copyright 2023",
        "",
        "import sys",
    ]
    result = _remove_existing_header(lines, "#")
    assert result == ["import sys"], "Failed to remove multi-line header"

    # Test when no header exists
    lines = ["import sys", "print('Hello')"]
    result = _remove_existing_header(lines, "#")
    assert result == lines, "Modified content when no header exists"


def test_merge_headers():
    """Test merging existing headers with our standard format."""
    # Test merging header with additional information
    existing = "# File: old_path.py\n# Author: John Doe\n# Version: 1.0"
    new = "File: test.py"
    result = _merge_headers(existing, new, "#", "")

    # Check that our file path is used but other information is preserved
    assert "File: test.py" in result, "New file path not in merged header"
    assert "Author: John Doe" in result, "Author info not preserved"
    assert "Version: 1.0" in result, "Version info not preserved"

    # Test with HTML-style comments
    existing = "<!-- Filename: old.html -->\n<!-- Created: 2023-07-01 -->"
    new = "File: test.html"
    result = _merge_headers(existing, new, "<!--", "-->")

    assert "File: test.html" in result, "New file path not in merged HTML header"
    assert "Created: 2023-07-01" in result, "Creation date not preserved in HTML header"


def test_web_framework_files():
    """Test processing web framework files like Vue and Svelte."""
    # Test Vue file with template
    vue_file = TEST_DIR / "vue" / "Component.vue"

    # Process the file
    process_file(vue_file, TEST_DIR)

    # Read and check the processed content
    processed = vue_file.read_text()
    assert "<template>" in processed, "Vue template element not preserved at top"
    assert "<!-- File: vue/Component.vue -->" in processed, "Vue file header not added correctly"

    # Test Vue file with script setup
    vue_setup_file = TEST_DIR / "vue" / "SetupComponent.vue"

    # Process the file
    process_file(vue_setup_file, TEST_DIR)

    # Read and check the processed content
    processed = vue_setup_file.read_text()
    assert "<script setup>" in processed, "Vue script setup not preserved at top"
    assert (
        "<!-- File: vue/SetupComponent.vue -->" in processed
    ), "Vue file header not added correctly"


def test_svelte_file():
    """Test processing Svelte files."""
    svelte_file = TEST_DIR / "svelte" / "Component.svelte"

    # Process the file
    process_file(svelte_file, TEST_DIR)

    # Read and check the processed content
    processed = svelte_file.read_text()
    assert "<script>" in processed, "Svelte script tag not preserved at top"
    assert (
        "<!-- File: svelte/Component.svelte -->" in processed
    ), "Svelte file header not added correctly"


def test_astro_file():
    """Test processing Astro files."""
    astro_file = TEST_DIR / "astro" / "Component.astro"
    # Process the file
    process_file(astro_file, TEST_DIR)

    # Read and check the processed content
    processed = astro_file.read_text()
    assert "---" in processed, "Astro frontmatter not preserved"
    assert (
        "<!-- File: astro/Component.astro -->" in processed
    ), "Astro file header not added correctly"


def test_react_jsx_file():
    """Test processing React JSX files."""
    react_file = TEST_DIR / "react" / "Counter.jsx"
    # Process the file
    process_file(react_file, TEST_DIR)

    # Read and check the processed content
    processed = react_file.read_text()
    assert processed.startswith("// File: react/Counter.jsx"), "JSX file header not added correctly"
    assert "import React" in processed, "JSX import statement not preserved"


def test_different_header_formats():
    """Test handling files with different header formats than our standard."""
    # Test JS file with non-standard header
    js_file = TEST_DIR / "legacy" / "legacy-component.js"
    # Save original content for comparison
    original_content = js_file.read_text()
    assert (
        "// Version: 1.0.0" in original_content
    ), "Test setup: Version info missing in original file"

    # Process the file
    process_file(js_file, TEST_DIR)

    # Verify the header was replaced with our format but preserved information
    processed = js_file.read_text()

    # Debug output if test fails
    if not processed.startswith("// File: legacy/legacy-component.js"):
        print("\nExpected header not found. Actual content starts with:")
        print(processed[:100])

    if "// Version: 1.0.0" not in processed:
        print("\nVersion info not preserved. Header content:")
        header_lines = [line for line in processed.splitlines()[:10] if line.strip()]
        print("\n".join(header_lines))

    # Check file header format and preserved metadata
    assert processed.startswith(
        "// File: legacy/legacy-component.js"
    ), "Header not converted to our format"
    assert "// Author: Legacy Developer" in processed, "Author information not preserved"
    assert "// Created: 2022-01-01" in processed, "Creation date not preserved"
    assert "// Version: 1.0.0" in processed, "Version info not preserved"

    # Check that actual content is preserved
    assert "class LegacyComponent" in processed, "Class content preserved"
    assert "incrementCount()" in processed, "Method content preserved"

    # Test CSS file with non-standard header
    css_file = TEST_DIR / "legacy" / "styles.css"

    # Process the file
    process_file(css_file, TEST_DIR)

    # Verify the header was replaced with our format but preserved information
    processed = css_file.read_text()
    assert processed.startswith(
        "/* File: legacy/styles.css */"
    ), "Header not converted to our format"
    assert "Description: Main stylesheet" in processed, "Description not preserved"
    assert "Author: Design Team" in processed, "Author information not preserved"

    # Check that CSS content is preserved
    assert ":root {" in processed, "CSS root block preserved"
    assert "--primary-color: #4a90e2;" in processed, "CSS variables preserved"


def test_html_doctype_handling():
    """Test that HTML DOCTYPE declarations are properly preserved."""
    html_file = TEST_DIR / "html" / "index.html"
    # Process the file
    process_file(html_file, TEST_DIR)

    # Read and check the processed content
    processed = html_file.read_text()
    lines = processed.splitlines()

    # Get non-empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Verify DOCTYPE is preserved at the top
    assert "<!DOCTYPE html>" in non_empty_lines[0], "DOCTYPE not preserved at the first line"
    # Verify our header appears right after the DOCTYPE
    assert "<!-- File: html/index.html -->" in non_empty_lines[1], "Header not placed after DOCTYPE"

    # Make sure the rest of the content is preserved
    assert '<html lang="en">' in processed, "HTML element not preserved"
    assert "<title>Sample Page</title>" in processed, "Title not preserved"


def test_skipped_file_types():
    """Test that specific file types are skipped."""
    # Create markdown and JSON files
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

    # Process the files
    process_file(md_file, TEST_DIR)
    process_file(json_file, TEST_DIR)
    # Verify the content is unchanged (markdown and JSON files should be skipped)
    assert md_file.read_text() == md_content, "Markdown file was modified but should be skipped"
    assert json_file.read_text() == json_content, "JSON file was modified but should be skipped"
