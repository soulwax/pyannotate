# File: tests/test_annotate_headers.py
# pylint: disable=too-few-public-methods

"""Core tests for the annotate_headers functionality."""

from pathlib import Path

import pytest

from pyannotate.annotate_headers import _get_comment_style, process_file, walk_directory
from tests.test_utils import (
    cleanup_test_directory,
    create_temp_test_directory,
    prepare_existing_header_js,
)

# Directory for temporary test files
TEST_DIR = Path("tests/sample_files")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    create_temp_test_directory(TEST_DIR)

    # Create basic test files
    (TEST_DIR / "valid_file.py").write_text("# Existing header\nprint('Hello, World!')\n")
    (TEST_DIR / "valid_file.js").write_text("// Old Header\nconsole.log('Hello, World!');\n")
    (TEST_DIR / "unsupported_file.dat").write_text("No comments here")

    # Create nested directory structure
    nested_dir = TEST_DIR / "nested"
    nested_dir.mkdir()
    (nested_dir / "script.sh").write_text('#!/bin/bash\necho "Nested!"\n')

    # Create binary test file
    binary_dir = TEST_DIR / "binary"
    binary_dir.mkdir()
    with open(binary_dir / "test.bin", "wb") as f:
        f.write(b"\x00\x01\x02\x03")

    yield

    # Cleanup after tests
    cleanup_test_directory(TEST_DIR)


class TestBasicFileProcessing:
    """Test basic file processing functionality."""

    def test_python_file_processing(self):
        """Test processing Python files."""
        file_path = TEST_DIR / "valid_file.py"
        process_file(file_path, TEST_DIR)
        content = file_path.read_text()
        assert content.startswith(
            "# File: valid_file.py\n"
        ), "Header not added correctly for .py file"
        assert "print('Hello, World!')" in content, "Original content preserved"

    def test_javascript_file_processing(self):
        """Test processing JavaScript files."""
        file_path = TEST_DIR / "valid_file.js"
        process_file(file_path, TEST_DIR)
        content = file_path.read_text()
        assert content.startswith(
            "// File: valid_file.js\n"
        ), "Header not added correctly for .js file"
        assert "console.log('Hello, World!');" in content, "Original content preserved"

    def test_unsupported_file_type_skipped(self):
        """Test that unsupported file types are skipped."""
        file_path = TEST_DIR / "unsupported_file.dat"
        original_content = file_path.read_text()
        process_file(file_path, TEST_DIR)
        content = file_path.read_text()
        assert content == original_content, "Unsupported file should not be modified"
        assert "File:" not in content, "Header should not be added to unsupported file type"

    def test_binary_file_detection_and_skipping(self):
        """Test that binary files are detected and skipped."""
        binary_file = TEST_DIR / "binary" / "test.bin"

        # Process the binary file
        process_file(binary_file, TEST_DIR)

        # Content should remain unchanged
        with open(binary_file, "rb") as f:
            content = f.read()
        assert content == b"\x00\x01\x02\x03", "Binary file was modified"


class TestShebangHandling:
    """Test handling of files with shebang lines."""

    def test_shebang_preservation(self):
        """Test that shebang lines are preserved."""
        file_path = TEST_DIR / "nested" / "script.sh"

        # Verify initial shebang
        original_content = file_path.read_text()
        assert original_content.startswith("#!/bin/bash\n"), "Initial shebang check failed"

        # Process the file
        process_file(file_path, TEST_DIR)
        updated_content = file_path.read_text()

        # Verify shebang preservation and header addition
        lines = updated_content.splitlines()
        assert lines[0] == "#!/bin/bash", "Shebang line not preserved"
        assert lines[1] == "# File: nested/script.sh", "Header not added after shebang"
        assert 'echo "Nested!"' in updated_content, "Script content preserved"

        # Verify no duplication
        assert len(updated_content.split("#!/bin/bash")) == 2, "Multiple shebang lines found"
        assert len(updated_content.split("File: nested/script.sh")) == 2, "Multiple headers found"


class TestXMLAndHTMLFiles:
    """Test handling of XML and HTML files with special declarations."""

    def test_html_with_doctype(self):
        """Test HTML files with DOCTYPE declarations."""
        html_file = TEST_DIR / "test.html"
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test</title>
</head>
<body>
    <h1>Test</h1>
</body>
</html>"""
        html_file.write_text(html_content)
        process_file(html_file, TEST_DIR)

        processed_content = html_file.read_text()
        lines = processed_content.splitlines()

        assert lines[0] == "<!DOCTYPE html>", "DOCTYPE not preserved as first line"
        assert lines[1] == "<!-- File: test.html -->", "Header not on second line"
        assert '<html lang="en">' in processed_content, "HTML content preserved"

    def test_xml_with_declaration(self):
        """Test XML files with XML declarations."""
        xml_file = TEST_DIR / "test.xml"
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item>Test</item>
</root>"""
        xml_file.write_text(xml_content)
        process_file(xml_file, TEST_DIR)

        processed_content = xml_file.read_text()
        lines = processed_content.splitlines()

        assert lines[0] == '<?xml version="1.0" encoding="UTF-8"?>', "XML declaration not preserved"
        assert lines[1] == "<!-- File: test.xml -->", "Header not on second line"
        assert "<root>" in processed_content, "XML content preserved"


class TestCommentStyleDetection:
    """Test comment style detection for various file types."""

    def test_python_comment_style(self):
        """Test Python comment style detection."""
        py_file = TEST_DIR / "test.py"
        py_file.write_text("print('test')")
        comment_style = _get_comment_style(py_file)
        assert comment_style == ("#", ""), "Incorrect comment style for Python"

    def test_javascript_comment_style(self):
        """Test JavaScript comment style detection."""
        js_file = TEST_DIR / "test.js"
        js_file.write_text("console.log('test');")
        comment_style = _get_comment_style(js_file)
        assert comment_style == ("//", ""), "Incorrect comment style for JavaScript"

    def test_css_comment_style(self):
        """Test CSS comment style detection."""
        css_file = TEST_DIR / "test.css"
        css_file.write_text("body { margin: 0; }")
        comment_style = _get_comment_style(css_file)
        assert comment_style == ("/*", "*/"), "Incorrect comment style for CSS"

    def test_html_comment_style(self):
        """Test HTML comment style detection."""
        html_file = TEST_DIR / "test.html"
        html_file.write_text("<html></html>")
        comment_style = _get_comment_style(html_file)
        assert comment_style == ("<!--", "-->"), "Incorrect comment style for HTML"

    def test_unsupported_file_comment_style(self):
        """Test that unsupported files return None for comment style."""
        dat_file = TEST_DIR / "test.dat"
        dat_file.write_text("some data")
        comment_style = _get_comment_style(dat_file)
        assert comment_style is None, "Unsupported file should return None for comment style"


class TestDirectoryTraversal:
    """Test directory traversal and recursive processing."""

    def test_walk_directory_processes_all_files(self):
        """Test that directory traversal processes all supported files."""
        # Process the entire test directory
        walk_directory(TEST_DIR, TEST_DIR)

        # Check that supported files were processed
        py_file = TEST_DIR / "valid_file.py"
        js_file = TEST_DIR / "valid_file.js"
        sh_file = TEST_DIR / "nested" / "script.sh"

        assert py_file.read_text().startswith("# File: valid_file.py"), "Python file not processed"
        assert js_file.read_text().startswith(
            "// File: valid_file.js"
        ), "JavaScript file not processed"
        assert "# File: nested/script.sh" in sh_file.read_text(), "Shell script not processed"

    def test_ignored_directories_are_skipped(self):
        """Test that ignored directories are not processed."""
        # Create an ignored directory
        ignored_dir = TEST_DIR / "node_modules"
        ignored_dir.mkdir()
        ignored_file = ignored_dir / "ignored_file.py"
        original_content = "print('This should not be processed')"
        ignored_file.write_text(original_content)

        # Process the directory
        walk_directory(TEST_DIR, TEST_DIR)

        # Verify the ignored file was not processed
        content = ignored_file.read_text()
        assert content == original_content, "File in ignored directory was processed"
        assert "File:" not in content, "Header added to file in ignored directory"


class TestUTF8Handling:
    """Test UTF-8 encoding handling."""

    def test_utf8_file_processing(self):
        """Test handling of UTF-8 encoded files with special characters."""
        utf8_file = TEST_DIR / "test_utf8.cpp"
        content = """// Some UTF-8 content with special characters
void showMessage() {
    std::cout << "Hello, 世界!" << std::endl;
}
"""
        utf8_file.write_text(content, encoding="utf-8")

        # Process the file
        process_file(utf8_file, TEST_DIR)

        # Read and verify content
        processed_content = utf8_file.read_text(encoding="utf-8")
        assert "世界" in processed_content, "UTF-8 characters were not preserved"
        assert processed_content.startswith("// File: test_utf8.cpp"), "Header not added correctly"
        assert "Hello, 世界!" in processed_content, "Original content not preserved"


class TestQtFiles:
    """Test handling of Qt-specific file types."""

    def test_qt_project_file(self):
        """Test handling of Qt project files (.pro)."""
        pro_file = TEST_DIR / "test.pro"
        content = """QT += core gui widgets
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = TestApp
TEMPLATE = app

SOURCES += main.cpp
HEADERS += mainwindow.h
"""
        pro_file.write_text(content)
        process_file(pro_file, TEST_DIR)

        processed_content = pro_file.read_text()
        assert processed_content.startswith("# File: test.pro"), "Qt project file header not added"
        assert "QT += core gui widgets" in processed_content, "Qt project content preserved"
        assert "TARGET = TestApp" in processed_content, "Qt project content preserved"

    def test_qt_ui_file(self):
        """Test handling of Qt UI files (.ui)."""
        ui_file = TEST_DIR / "test.ui"
        content = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
 </widget>
</ui>"""
        ui_file.write_text(content)
        process_file(ui_file, TEST_DIR)

        processed_content = ui_file.read_text()
        lines = processed_content.splitlines()

        assert lines[0] == '<?xml version="1.0" encoding="UTF-8"?>', "XML declaration preserved"
        assert "<!-- File: test.ui -->" in processed_content, "UI file header not added"
        assert "<class>MainWindow</class>" in processed_content, "UI file content preserved"

    def test_qt_translation_file(self):
        """Test that Qt translation files (.ts) are handled correctly."""
        ts_file = TEST_DIR / "translation.ts"
        content = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="zh_CN">
    <context>
        <name>MainWindow</name>
        <message>
            <source>Hello</source>
            <translation>你好</translation>
        </message>
    </context>
</TS>"""
        ts_file.write_text(content, encoding="utf-8")
        process_file(ts_file, TEST_DIR)

        processed_content = ts_file.read_text(encoding="utf-8")
        lines = processed_content.splitlines()

        assert lines[0] == '<?xml version="1.0" encoding="utf-8"?>', "XML declaration preserved"
        assert (
            "<!-- File: translation.ts -->" in processed_content
        ), "Translation file header not added"
        assert (
            "<translation>你好</translation>" in processed_content
        ), "Translation content preserved"


class TestPowerShellFiles:
    """Test handling of PowerShell files with various comment patterns."""

    def test_powershell_comment_style_detection(self):
        """Test PowerShell file pattern recognition."""
        ps_file = TEST_DIR / "test.ps1"
        ps_file.write_text('Write-Host "Testing"')

        comment_style = _get_comment_style(ps_file)
        assert comment_style is not None, "PowerShell file pattern not recognized"
        assert comment_style == ("#", ""), "Incorrect comment style for PowerShell"

    def test_powershell_with_existing_comments(self):
        """Test processing PowerShell files while preserving existing comments."""
        ps_file = TEST_DIR / "test_preserve.ps1"
        ps_content = """# This is an important PowerShell script comment
# With multiple comment lines
# That should be preserved
Write-Host "Hello, World!" """
        ps_file.write_text(ps_content)
        process_file(ps_file, TEST_DIR)
        processed_content = ps_file.read_text()

        # Split content into lines for easier testing
        content_lines = processed_content.splitlines()

        # Verify structure
        assert content_lines[0].startswith("# File: test_preserve.ps1"), "Header not on first line"
        assert content_lines[1] == "", "No blank line after header"
        assert (
            content_lines[2] == "# This is an important PowerShell script comment"
        ), "First comment not preserved"
        assert "That should be preserved" in processed_content, "Comments not preserved"
        assert "Write-Host" in processed_content, "Code content preserved"

        # Verify no duplicate header
        headers = [line for line in content_lines if "File: test_preserve.ps1" in line]
        assert len(headers) == 1, "Multiple headers found"

    def test_powershell_multiline_metadata(self):
        """Test processing PowerShell files with multiline comments at the top."""
        ps_file = TEST_DIR / "test_multiline.ps1"
        ps_content = """# PowerShell Backup Script V2.1
# Enhanced version with wildcard support and improved config handling
# Created by: John Doe
# Last modified: 2024-01-05

Write-Host "Backup script starting..."
"""
        ps_file.write_text(ps_content)
        process_file(ps_file, TEST_DIR)
        processed_content = ps_file.read_text()

        # Verify the structure
        lines = processed_content.splitlines()
        assert lines[0].startswith("# File: test_multiline.ps1"), "Header not at top"
        assert lines[1] == "", "No blank line after header"
        assert "# PowerShell Backup Script V2.1" in lines[2], "First comment line not preserved"
        assert "# Enhanced version" in lines[3], "Second comment line not preserved"
        assert "# Created by: John Doe" in lines[4], "Third comment line not preserved"
        assert "Write-Host" in processed_content, "Original code not preserved"


class TestSpecialConfigFiles:
    """Test handling of special configuration files."""

    def test_gitignore_file(self):
        """Test processing .gitignore files."""
        gitignore_file = TEST_DIR / ".gitignore"
        gitignore_content = """# Ignore these files
__pycache__/
*.py[cod]
*$py.class
.env
"""
        gitignore_file.write_text(gitignore_content)
        process_file(gitignore_file, TEST_DIR)
        processed_content = gitignore_file.read_text()

        assert processed_content.startswith(
            "# File: .gitignore"
        ), "Header not added correctly for .gitignore"
        assert "# Ignore these files" in processed_content, "Original content preserved"
        assert "__pycache__/" in processed_content, "Gitignore rules preserved"

    def test_makefile(self):
        """Test processing Makefile."""
        makefile = TEST_DIR / "Makefile"
        makefile_content = """# Makefile for sample project
CC = gcc
CFLAGS = -Wall -g
TARGET = sample

all: $(TARGET)

clean:
\trm -f $(TARGET)
"""
        makefile.write_text(makefile_content)
        process_file(makefile, TEST_DIR)
        processed_content = makefile.read_text()

        assert processed_content.startswith(
            "# File: Makefile"
        ), "Header not added correctly for Makefile"
        assert "CC = gcc" in processed_content, "Makefile content preserved"
        assert "clean:" in processed_content, "Makefile targets preserved"

    def test_dockerfile(self):
        """Test processing Dockerfile."""
        dockerfile = TEST_DIR / "Dockerfile"
        dockerfile_content = """FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -e .

CMD ["python", "-m", "pyannotate"]
"""
        dockerfile.write_text(dockerfile_content)
        process_file(dockerfile, TEST_DIR)
        processed_content = dockerfile.read_text()

        assert processed_content.startswith(
            "# File: Dockerfile"
        ), "Header not added correctly for Dockerfile"
        assert "FROM python:3.10-slim" in processed_content, "Dockerfile content preserved"
        assert "WORKDIR /app" in processed_content, "Dockerfile commands preserved"

    def test_pyproject_toml(self):
        """Test processing pyproject.toml files."""
        pyproject_file = TEST_DIR / "pyproject.toml"
        pyproject_content = """[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm>=6.2"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
"""
        pyproject_file.write_text(pyproject_content)
        process_file(pyproject_file, TEST_DIR)
        processed_content = pyproject_file.read_text()

        assert processed_content.startswith(
            "# File: pyproject.toml"
        ), "Header not added correctly for pyproject.toml"
        assert "[build-system]" in processed_content, "TOML content preserved"
        assert "[tool.black]" in processed_content, "TOML sections preserved"


class TestExistingHeaderHandling:
    """Test handling of files that already have headers."""

    def test_existing_header_replacement(self):
        """Test that existing headers are properly updated."""
        js_file = prepare_existing_header_js(TEST_DIR)

        # Process the file
        process_file(js_file, TEST_DIR)

        # Verify the header was replaced with our format but preserved information
        processed_content = js_file.read_text()

        assert processed_content.startswith(
            "// File: existing_header.js"
        ), "Header not converted to our format"
        assert "// Author: Someone" in processed_content, "Author information not preserved"
        assert "console.log" in processed_content, "Original code preserved"

    def test_no_duplicate_headers(self):
        """Test that processing a file twice doesn't create duplicate headers."""
        py_file = TEST_DIR / "duplicate_test.py"
        py_file.write_text("print('test')")

        # Process twice
        process_file(py_file, TEST_DIR)
        first_content = py_file.read_text()
        process_file(py_file, TEST_DIR)
        second_content = py_file.read_text()

        # Content should be identical after second processing
        assert first_content == second_content, "Second processing should not change content"

        # Should have exactly one header
        header_count = second_content.count("File: duplicate_test.py")
        assert header_count == 1, f"Should have exactly 1 header, found {header_count}"

    def test_css_existing_annotation_preserved(self):
        """Ensure existing CSS single-line block annotations are not corrupted.

        A CSS file that already contains a comment like
        "/* src/styles/globals.css */" should not get an extra closing
        "*/" inserted by the annotation logic.
        """
        css_file = TEST_DIR / "globals.css"
        # Simulate a file that already contains a single-line block annotation
        css_file.write_text("/* src/styles/globals.css */\nbody { color: red; }\n")

        # Process the file
        process_file(css_file, TEST_DIR)

        processed = css_file.read_text()

        # Ensure we didn't create a broken comment like "*/ */"
        assert "*/ */" not in processed, "Found duplicated comment closers in CSS header"

        # Original annotation should still be present
        assert "src/styles/globals.css" in processed, "Original annotation text was lost"

        # CSS content preserved
        assert "body { color: red; }" in processed, "CSS body was lost"

    def test_css_existing_annotation_preserved_with_repo_root(self):
        """Ensure CSS annotations are preserved when the project_root is the repo root.

        This mirrors running the CLI from the repository root where header lines
        include the full relative path (e.g. "tests/sample_files/globals.css").
        """
        css_file = TEST_DIR / "globals.css"
        css_file.write_text("/* src/styles/globals.css */\nbody { color: red; }\n")

        # Process using repo root so header will contain the relative path
        process_file(css_file, Path('.').resolve())

        processed = css_file.read_text()

        # Ensure we didn't create a broken comment like "*/ */"
        assert "*/ */" not in processed, "Found duplicated comment closers when using repo root"

        # Header should include the path
        expected_path = "tests/sample_files/globals.css"
        assert expected_path in processed, "Header path missing when using repo root"

        # Original annotation and body preserved
        assert "src/styles/globals.css" in processed
        assert "body { color: red; }" in processed
