# Testing PyAnnotate

This document outlines how to run tests for the PyAnnotate project.

## Automated Testing

We've included automated scripts to make testing easier. These scripts run:

1. Code formatting (black)
2. Linting (pylint)
3. Unit tests (pytest with coverage)

### Prerequisites

Make sure you have the development dependencies installed:

```bash
pip install -r requirements-dev.txt
```

### Running Tests

#### On Windows

```
run_tests.bat
```

#### On Unix/Linux/macOS

```
./run_tests.sh
```

Or directly with Python:

```
python run_tests.py
```

### Test Output

The automated test script will create:

- `pylint.txt` - Linting output
- `pytest.txt` - Test results and coverage information

## Running Tests Manually

If you prefer to run tests manually:

### Format Code

```bash
black .
```

### Run Linter

```bash
pylint src tests > pylint.txt
```

### Run Tests with Coverage

```bash
pytest --cov=pyannotate tests/ > pytest.txt
```

### Run a Specific Test

```bash
pytest tests/test_enhanced_headers.py::test_web_framework_files
```

## Test Coverage

The test coverage report is generated automatically when running tests. You can find the coverage information in the `pytest.txt` file or in the terminal output.

## Testing Web Framework Support

The enhanced header functionality includes support for modern web frameworks like Vue, Svelte, and Astro.

To specifically test these features, use:

```bash
pytest tests/test_enhanced_headers.py::test_web_framework_files
```

## Troubleshooting

If tests are failing:

1. Make sure all dependencies are installed correctly
2. Check the exact error messages in `pytest.txt`
3. Inspect the linting issues in `pylint.txt`
4. Run specific test files or functions to isolate the issue
