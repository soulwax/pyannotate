# File: tests/test_annotate_headers.py
from pathlib import Path
import shutil
import pytest
from pyannotate.annotate_headers import process_file, walk_directory

# Directory for temporary test files
TEST_DIR = Path("tests/sample_files")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True)
    # Create sample files
    (TEST_DIR / "valid_file.py").write_text("# Existing header\nprint('Hello, World!')\n")
    (TEST_DIR / "valid_file.js").write_text("// Old Header\nconsole.log('Hello, World!');\n")
    (TEST_DIR / "invalid_file.dat").write_text("No comments here")
    nested_dir = TEST_DIR / "nested"
    nested_dir.mkdir()
    (nested_dir / "valid_nested_file.sh").write_text('#!/bin/bash\necho "Nested!"\n')
    yield
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
