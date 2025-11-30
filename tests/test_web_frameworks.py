# File: tests/test_web_frameworks.py
# pylint: disable=duplicate-code

"""Tests for web framework and templating language support."""

from pathlib import Path

import pytest

from pyannotate.annotate_headers import _get_comment_style, process_file
from tests.test_utils import cleanup_test_directory, create_temp_test_directory

# Directory for temporary test files
TEST_DIR = Path("tests/sample_files")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    create_temp_test_directory(TEST_DIR)
    yield
    cleanup_test_directory(TEST_DIR)


class TestHandlebars:
    """Test Handlebars template support."""

    def test_handlebars_comment_style(self):
        """Test Handlebars comment style detection."""
        hbs_file = TEST_DIR / "test.hbs"
        hbs_file.write_text("<div>{{title}}</div>")
        comment_style = _get_comment_style(hbs_file)
        assert comment_style == ("<!--", "-->"), "Incorrect comment style for Handlebars"

    def test_handlebars_file_processing(self):
        """Test processing Handlebars files."""
        hbs_file = TEST_DIR / "test.hbs"
        hbs_file.write_text("<div>{{title}}</div>")
        process_file(hbs_file, TEST_DIR)
        content = hbs_file.read_text()
        assert content.startswith(
            "<!-- File: test.hbs -->"
        ), "Header not added correctly for Handlebars"

    def test_handlebars_extension(self):
        """Test .handlebars extension support."""
        handlebars_file = TEST_DIR / "test.handlebars"
        handlebars_file.write_text("<div>{{content}}</div>")
        comment_style = _get_comment_style(handlebars_file)
        assert comment_style == ("<!--", "-->"), "Incorrect comment style for .handlebars"


class TestEJS:
    """Test EJS template support."""

    def test_ejs_comment_style(self):
        """Test EJS comment style detection."""
        ejs_file = TEST_DIR / "test.ejs"
        ejs_file.write_text("<div><%= title %></div>")
        comment_style = _get_comment_style(ejs_file)
        assert comment_style == ("<!--", "-->"), "Incorrect comment style for EJS"

    def test_ejs_file_processing(self):
        """Test processing EJS files."""
        ejs_file = TEST_DIR / "test.ejs"
        ejs_file.write_text("<div><%= title %></div>")
        process_file(ejs_file, TEST_DIR)
        content = ejs_file.read_text()
        assert content.startswith("<!-- File: test.ejs -->"), "Header not added correctly for EJS"


class TestPug:
    """Test Pug/Jade template support."""

    def test_pug_comment_style(self):
        """Test Pug comment style detection."""
        pug_file = TEST_DIR / "test.pug"
        pug_file.write_text("div.container\n  h1= title")
        comment_style = _get_comment_style(pug_file)
        assert comment_style == ("//", ""), "Incorrect comment style for Pug"

    def test_pug_file_processing(self):
        """Test processing Pug files."""
        pug_file = TEST_DIR / "test.pug"
        pug_file.write_text("div.container\n  h1= title")
        process_file(pug_file, TEST_DIR)
        content = pug_file.read_text()
        assert content.startswith("// File: test.pug"), "Header not added correctly for Pug"

    def test_jade_extension(self):
        """Test .jade extension support."""
        jade_file = TEST_DIR / "test.jade"
        jade_file.write_text("div.container\n  p= content")
        comment_style = _get_comment_style(jade_file)
        assert comment_style == ("//", ""), "Incorrect comment style for Jade"


class TestMustache:
    """Test Mustache template support."""

    def test_mustache_comment_style(self):
        """Test Mustache comment style detection."""
        mustache_file = TEST_DIR / "test.mustache"
        mustache_file.write_text("<div>{{title}}</div>")
        comment_style = _get_comment_style(mustache_file)
        assert comment_style == ("<!--", "-->"), "Incorrect comment style for Mustache"

    def test_mustache_file_processing(self):
        """Test processing Mustache files."""
        mustache_file = TEST_DIR / "test.mustache"
        mustache_file.write_text("<div>{{title}}</div>")
        process_file(mustache_file, TEST_DIR)
        content = mustache_file.read_text()
        assert content.startswith(
            "<!-- File: test.mustache -->"
        ), "Header not added correctly for Mustache"

    def test_mst_extension(self):
        """Test .mst extension support."""
        mst_file = TEST_DIR / "test.mst"
        mst_file.write_text("<div>{{content}}</div>")
        comment_style = _get_comment_style(mst_file)
        assert comment_style == ("<!--", "-->"), "Incorrect comment style for .mst"


class TestTwig:
    """Test Twig template support."""

    def test_twig_comment_style(self):
        """Test Twig comment style detection."""
        twig_file = TEST_DIR / "test.twig"
        twig_file.write_text("<div>{{ title }}</div>")
        comment_style = _get_comment_style(twig_file)
        assert comment_style == ("{#", "#}"), "Incorrect comment style for Twig"

    def test_twig_file_processing(self):
        """Test processing Twig files."""
        twig_file = TEST_DIR / "test.twig"
        twig_file.write_text("<div>{{ title }}</div>")
        process_file(twig_file, TEST_DIR)
        content = twig_file.read_text()
        assert content.startswith("{# File: test.twig #}"), "Header not added correctly for Twig"


class TestJinja2:
    """Test Jinja2 template support."""

    def test_jinja_comment_style(self):
        """Test Jinja comment style detection."""
        jinja_file = TEST_DIR / "test.jinja"
        jinja_file.write_text("<div>{{ title }}</div>")
        comment_style = _get_comment_style(jinja_file)
        assert comment_style == ("{#", "#}"), "Incorrect comment style for Jinja"

    def test_jinja_file_processing(self):
        """Test processing Jinja files."""
        jinja_file = TEST_DIR / "test.jinja"
        jinja_file.write_text("<div>{{ title }}</div>")
        process_file(jinja_file, TEST_DIR)
        content = jinja_file.read_text()
        assert content.startswith("{# File: test.jinja #}"), "Header not added correctly for Jinja"

    def test_jinja2_extension(self):
        """Test .jinja2 extension support."""
        jinja2_file = TEST_DIR / "test.jinja2"
        jinja2_file.write_text("<div>{{ content }}</div>")
        comment_style = _get_comment_style(jinja2_file)
        assert comment_style == ("{#", "#}"), "Incorrect comment style for .jinja2"


class TestMDX:
    """Test MDX file support."""

    def test_mdx_comment_style(self):
        """Test MDX comment style detection."""
        mdx_file = TEST_DIR / "test.mdx"
        mdx_file.write_text("# My Article\n\n<Component />")
        comment_style = _get_comment_style(mdx_file)
        assert comment_style == ("<!--", "-->"), "Incorrect comment style for MDX"

    def test_mdx_file_processing(self):
        """Test processing MDX files."""
        mdx_file = TEST_DIR / "test.mdx"
        mdx_file.write_text("# My Article\n\n<Component />")
        process_file(mdx_file, TEST_DIR)
        content = mdx_file.read_text()
        assert content.startswith("<!-- File: test.mdx -->"), "Header not added correctly for MDX"


class TestWebFrameworkIntegration:
    """Integration tests for web framework files with existing content."""

    def test_handlebars_with_existing_content(self):
        """Test Handlebars file with template structure."""
        hbs_file = TEST_DIR / "component.hbs"
        hbs_file.write_text(
            "<div class='component'>\n  <h1>{{title}}</h1>\n  <p>{{description}}</p>\n</div>"
        )
        process_file(hbs_file, TEST_DIR)
        content = hbs_file.read_text()
        assert "<!-- File: component.hbs -->" in content
        assert "{{title}}" in content
        assert "{{description}}" in content

    def test_pug_with_existing_content(self):
        """Test Pug file with indentation structure."""
        pug_file = TEST_DIR / "layout.pug"
        pug_file.write_text("doctype html\nhtml\n  head\n    title= pageTitle")
        process_file(pug_file, TEST_DIR)
        content = pug_file.read_text()
        assert content.startswith("// File: layout.pug")
        assert "doctype html" in content

    def test_twig_with_existing_content(self):
        """Test Twig file with template syntax."""
        twig_file = TEST_DIR / "template.twig"
        twig_file.write_text(
            "<!DOCTYPE html>\n<html>\n<body>\n  <h1>{{ heading }}</h1>\n</body>\n</html>"
        )
        process_file(twig_file, TEST_DIR)
        content = twig_file.read_text()
        assert content.startswith("{# File: template.twig #}")
        assert "{{ heading }}" in content

    def test_ejs_with_script_tags(self):
        """Test EJS file with script tags."""
        ejs_file = TEST_DIR / "page.ejs"
        ejs_file.write_text(
            "<!DOCTYPE html>\n<html>\n<head>\n  <title><%= title %></title>\n</head>\n</html>"
        )
        process_file(ejs_file, TEST_DIR)
        content = ejs_file.read_text()
        assert "<!-- File: page.ejs -->" in content
        assert "<%= title %>" in content
