# File: tests/__init__.py

"""
Initialization for tests package.

This file can be used to:
- Set up shared fixtures
- Configure pytest plugins
- Add global test configurations
"""

# Import test utilities to make them available package-wide
from .test_utils import (
    COMMENT_STYLE_TEST_CASES,
    COMMON_IGNORED_FILES,
    ENV_FILE_NAMES,
    LICENSE_FILE_NAMES,
    WEB_FRAMEWORK_TEMPLATES,
    assert_file_content_unchanged,
    assert_header_added,
    cleanup_test_directory,
    create_temp_test_directory,
    create_test_file_with_header_processing,
)

__all__ = [
    "WEB_FRAMEWORK_TEMPLATES",
    "COMMENT_STYLE_TEST_CASES",
    "ENV_FILE_NAMES",
    "LICENSE_FILE_NAMES",
    "COMMON_IGNORED_FILES",
    "create_temp_test_directory",
    "cleanup_test_directory",
    "create_test_file_with_header_processing",
    "assert_file_content_unchanged",
    "assert_header_added",
]


def pytest_configure(config):
    """
    Pytest hook to perform additional configuration.

    This can be used to:
    - Add custom markers
    - Modify pytest settings
    """
    # Example: register a custom marker
    config.addinivalue_line("markers", "slow: mark test as slow-running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
