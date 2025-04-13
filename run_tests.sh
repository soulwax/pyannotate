#!/bin/bash
# run_tests.sh - Unix/Linux/macOS script to automate tests for PyAnnotate

echo "=== PyAnnotate Test Runner (Unix) ==="

# Check if Python is in the path
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 not found in PATH!"
    echo "Please install Python 3 or add it to your PATH."
    exit 1
fi

# Check if the test script exists
if [ ! -f "run_tests.py" ]; then
    echo "Error: run_tests.py not found!"
    echo "Please make sure you're running this from the project root."
    exit 1
fi

# Make sure the script is executable
chmod +x run_tests.py

# Run the test automation script
python3 run_tests.py

# Forward the exit code
exit $?
