# File: tests/__init__.py
"""
Initialization for tests package.

This file can be used to:
- Set up shared fixtures
- Configure pytest plugins
- Add global test configurations
"""

# Import any shared test utilities or fixtures
# from .test_utils import some_utility


# If you need to modify pytest configuration globally
def pytest_configure(config):
    """
    Pytest hook to perform additional configuration.

    This can be used to:
    - Add custom markers
    - Modify pytest settings
    """
    # Example: register a custom marker
    config.addinivalue_line("markers", "slow: mark test as slow-running")
