# File: tests/test_annotate_headers.py
from pathlib import Path
import shutil
import pytest
from pyannotate.annotate_headers import _get_comment_style, process_file, walk_directory

# Directory for temporary test files
TEST_DIR = Path("tests/sample_files")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True)

    # Create sample files for basic tests
    (TEST_DIR / "valid_file.py").write_text("# Existing header\nprint('Hello, World!')\n")
    (TEST_DIR / "valid_file.js").write_text("// Old Header\nconsole.log('Hello, World!');\n")
    (TEST_DIR / "invalid_file.dat").write_text("No comments here")

    # Create nested directory structure
    nested_dir = TEST_DIR / "nested"
    nested_dir.mkdir()
    (nested_dir / "valid_nested_file.sh").write_text('#!/bin/bash\necho "Nested!"\n')

    # Create Qt-specific test directories
    qt_project_dir = TEST_DIR / "qt_project"
    qt_project_dir.mkdir()

    # Create various Qt-related files
    pro_content = """QT += core gui widgets
TEMPLATE = app
SOURCES += main.cpp
"""
    (qt_project_dir / "test.pro").write_text(pro_content)

    ui_content = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
</ui>"""
    (qt_project_dir / "mainwindow.ui").write_text(ui_content)

    # Create binary-like files
    binary_dir = TEST_DIR / "binary"
    binary_dir.mkdir()
    with open(binary_dir / "test.bin", "wb") as f:
        f.write(b"\x00\x01\x02\x03")

    yield

    # Cleanup after tests
    shutil.rmtree(TEST_DIR)


def test_process_file():
    """Test processing individual files."""
    # Test Python file
    file_path = TEST_DIR / "valid_file.py"
    process_file(file_path, TEST_DIR)
    content = file_path.read_text()
    assert content.startswith("# File: valid_file.py\n"), "Header not added correctly for .py file"

    # Test JavaScript file
    file_path = TEST_DIR / "valid_file.js"
    process_file(file_path, TEST_DIR)
    content = file_path.read_text()
    assert content.startswith("// File: valid_file.js\n"), "Header not added correctly for .js file"

    # Test unsupported file type
    file_path = TEST_DIR / "invalid_file.dat"
    process_file(file_path, TEST_DIR)
    content = file_path.read_text()
    assert "File:" not in content, "Header added incorrectly for unsupported file type"

    # Test HTML file with DOCTYPE
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
    assert processed_content.startswith(
        "<!DOCTYPE html>\n<!-- File: test.html -->"
    ), "HTML DOCTYPE handling incorrect"
    assert (
        "<!DOCTYPE html>" in processed_content.splitlines()[0]
    ), "DOCTYPE not preserved as first line"
    assert "File: test.html" in processed_content.splitlines()[1], "Header not on second line"

    # Test XML file
    xml_file = TEST_DIR / "test.xml"
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item>Test</item>
</root>"""
    xml_file.write_text(xml_content)
    process_file(xml_file, TEST_DIR)
    processed_content = xml_file.read_text()
    assert processed_content.startswith(
        '<?xml version="1.0" encoding="UTF-8"?>'
    ), "XML declaration not preserved"
    assert "File: test.xml" in processed_content.splitlines()[1], "Header not on second line"


def test_powershell_preserve_comments():
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


def test_powershell_pattern_matching():
    """Test PowerShell file pattern recognition."""
    ps_file = TEST_DIR / "test_multi_comment.ps1"
    ps_content = """# PowerShell Backup Script V2.1
# Enhanced version with wildcard support and improved config handling
Write-Host "Testing pattern matching" """

    # Write test file
    ps_file.write_text(ps_content)

    # Test pattern recognition
    comment_style = _get_comment_style(ps_file)
    assert comment_style is not None, "PowerShell file pattern not recognized"
    assert comment_style == ("#", ""), "Incorrect comment style for PowerShell"

    # Process the file
    process_file(ps_file, TEST_DIR)
    processed_content = ps_file.read_text()

    # Split into lines for analysis
    lines = processed_content.splitlines()

    # Verify structure
    assert lines[0].startswith("# File:"), "Header not added"
    assert lines[1] == "", "No blank line after header"
    assert lines[2] == "# PowerShell Backup Script V2.1", "First comment line not preserved exactly"
    assert (
        lines[3] == "# Enhanced version with wildcard support and improved config handling"
    ), "Second comment line not preserved exactly"


def test_powershell_multiline_header():
    """Test processing PowerShell files with multiline comments at the top."""
    ps_file = TEST_DIR / "test_multiline.ps1"
    ps_content = """# PowerShell Backup Script V2.1
# Enhanced version with wildcard support and improved config handling
# Created by: John Doe
# Last modified: 2024-01-05

Write-Host "Backup script starting..."
"""
    ps_file.write_text(ps_content)

    # Process the file
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


def test_shell_file():
    """Test processing shell scripts."""
    sh_file = TEST_DIR / "test.sh"
    sh_content = """#!/bin/bash
echo "Hello, World!" """
    sh_file.write_text(sh_content)
    process_file(sh_file, TEST_DIR)
    processed_content = sh_file.read_text()
    assert processed_content.startswith(
        "#!/bin/bash\n# File: test.sh\n"
    ), "Header not added correctly for .sh file"
    assert "echo" in processed_content, "Script content lost"
    assert "Hello, World!" in processed_content, "Script content lost"


def test_walk_directory():
    """Test directory traversal and file processing."""
    walk_directory(TEST_DIR, TEST_DIR)

    py_file = TEST_DIR / "valid_file.py"
    js_file = TEST_DIR / "valid_file.js"
    sh_file = TEST_DIR / "nested/valid_nested_file.sh"

    # Read and check content
    sh_content = sh_file.read_text()
    assert sh_content.startswith("#!/bin/bash\n"), "Shebang line not found"
    assert "# File: nested/valid_nested_file.sh\n" in sh_content, "Header not found in shell script"

    assert py_file.read_text().startswith(
        "# File: valid_file.py\n"
    ), "Header not added correctly for .py file"
    assert js_file.read_text().startswith(
        "// File: valid_file.js\n"
    ), "Header not added correctly for .js file"


def test_shebang_preservation():
    """Ensure shebang lines are preserved."""
    file_path = TEST_DIR / "nested/valid_nested_file.sh"
    original_content = file_path.read_text()
    assert original_content.startswith("#!/bin/bash\n"), "Initial shebang check failed"

    process_file(file_path, TEST_DIR)
    updated_content = file_path.read_text()
    assert "#!/bin/bash\n" in updated_content, "Shebang line lost"
    assert "# File: nested/valid_nested_file.sh\n" in updated_content, "Header not found"
    assert len(updated_content.split("#!/bin/bash")) == 2, "Multiple shebang lines found"
    assert (
        len(updated_content.split("File: nested/valid_nested_file.sh")) == 2
    ), "Multiple headers found"


def test_existing_header_update():
    """Test updating existing headers."""
    file_path = TEST_DIR / "valid_file.js"
    process_file(file_path, TEST_DIR)
    updated_content = file_path.read_text()
    assert updated_content.startswith("// File: valid_file.js\n"), "Header not updated correctly"


def test_ignored_directories():
    """Ensure ignored directories are skipped."""
    ignored_dir = TEST_DIR / "node_modules"
    ignored_dir.mkdir()
    (ignored_dir / "ignored_file.py").write_text("print('This should not be processed')")

    walk_directory(TEST_DIR, TEST_DIR)

    ignored_file = ignored_dir / "ignored_file.py"
    content = ignored_file.read_text()
    assert "File:" not in content, "Ignored directory files should not be processed"


def test_binary_file_detection():
    """Test the binary file detection functionality."""
    binary_file = TEST_DIR / "test.bin"
    with open(binary_file, "wb") as f:
        f.write(b"\x00\x01\x02\x03")  # Write some binary content

    # Process the binary file
    process_file(binary_file, TEST_DIR)

    # Content should remain unchanged
    with open(binary_file, "rb") as f:
        content = f.read()
    assert content == b"\x00\x01\x02\x03", "Binary file was modified"


def test_utf8_file_handling():
    """Test handling of UTF-8 encoded files."""
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


def test_qt_project_file():
    """Test handling of Qt project files (.pro)."""
    pro_file = TEST_DIR / "test.pro"
    content = """QT += core gui widgets
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Waifu2x-Extension-GUI
TEMPLATE = app

SOURCES += main.cpp\\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui"""

    pro_file.write_text(content)
    process_file(pro_file, TEST_DIR)

    processed_content = pro_file.read_text()
    assert processed_content.startswith("# File: test.pro"), "Qt project file header not added"
    assert "QT += core gui widgets" in processed_content, "Qt project content preserved"


def test_qt_ui_file():
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
    assert (
        '<?xml version="1.0" encoding="UTF-8"?>' in processed_content.splitlines()[0]
    ), "XML declaration preserved"
    assert "<!-- File: test.ui -->" in processed_content, "UI file header not added"
    assert "<class>MainWindow</class>" in processed_content, "UI file content preserved"


def test_qt_resource_file():
    """Test handling of Qt resource files (.qrc)."""
    qrc_file = TEST_DIR / "resources.qrc"
    content = """<!DOCTYPE RCC>
<RCC version="1.0">
    <qresource prefix="/images">
        <file>icon/main.png</file>
        <file>icon/settings.png</file>
    </qresource>
</RCC>"""

    qrc_file.write_text(content)
    process_file(qrc_file, TEST_DIR)

    processed_content = qrc_file.read_text()
    assert "<!DOCTYPE RCC>" in processed_content.splitlines()[0], "DOCTYPE preserved"
    assert "<!-- File: resources.qrc -->" in processed_content, "Resource file header not added"
    assert "<RCC version=" in processed_content, "Resource file content preserved"


# Removed duplicate test_ignored_directories as it exists in the original tests


def test_qt_translation_file():
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
    assert (
        '<?xml version="1.0" encoding="utf-8"?>' in processed_content.splitlines()[0]
    ), "XML declaration preserved"
    assert "<!-- File: translation.ts -->" in processed_content, "Translation file header not added"
    assert "<translation>你好</translation>" in processed_content, "Translation content preserved"
