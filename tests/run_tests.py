# File: tests/run_tests.py
"""
Automated test script for PyAnnotate.
Runs code formatting, linting, and tests in one command.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, output_file=None):
    """Run a command and optionally save output to a file."""
    print(f"Running: {' '.join(cmd)}")

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdout=f, stderr=f, text=True, check=False)
    else:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    return result


def format_code():
    """Run black code formatter."""
    print("\n=== Running Code Formatter (black) ===")
    result = run_command(["black", "."])

    if result.returncode != 0:
        print("Code formatting failed!")
        if result.stderr:
            print(result.stderr)
        return False

    print("Code formatting successful")
    return True


def run_lint():
    """Run pylint on source and test files."""
    print("\n=== Running Linter (pylint) ===")
    pylint_out = "pylint.txt"
    result = run_command(["pylint", "src", "tests"], pylint_out)

    # We don't fail on lint errors, just report them
    with open(pylint_out, "r", encoding="utf-8") as f:
        content = f.read()

    if "Your code has been rated at 10.00/10" in content:
        print("Linting successful - Perfect score!")
        return True

    score_line = [line for line in content.splitlines() if "Your code has been rated at" in line]
    if score_line:
        print(f"Linting issues found: {score_line[0]}")
    else:
        print("Linting issues found. See pylint.txt for details.")
    return False


def run_tests():
    """Run pytest with coverage."""
    print("\n=== Running Tests (pytest) ===")
    pytest_out = "pytest.txt"
    result = run_command(["pytest", "--cov=pyannotate", "tests/"], pytest_out)

    if result.returncode != 0:
        print("Tests failed!")
        with open(pytest_out, "r", encoding="utf-8") as f:
            print(f.read())
        return False

    with open(pytest_out, "r", encoding="utf-8") as f:
        content = f.read()
        print("Test results summary:")
        for line in content.splitlines():
            if "collected" in line or "passed" in line or "TOTAL" in line:
                print(line)

    print("Tests completed successfully")
    return True


def main():
    """Main entry point."""
    print("=== PyAnnotate Automated Testing ===")

    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Run all steps
    format_success = format_code()
    lint_success = run_lint()
    test_success = run_tests()

    # Print summary
    print("\n=== Summary ===")
    print(f"Code formatting: {'✅ PASSED' if format_success else '❌ FAILED'}")
    print(f"Linting: {'✅ PASSED' if lint_success else '⚠️ WARNINGS'}")
    print(f"Tests: {'✅ PASSED' if test_success else '❌ FAILED'}")

    # Return overall success status
    if not (format_success and test_success):
        print("\n❌ Some checks failed!")
        return 1

    print("\n✅ All checks passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
