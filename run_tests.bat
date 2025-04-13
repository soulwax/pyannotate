@echo off
REM run_tests.bat - Windows script to automate tests for PyAnnotate

echo === PyAnnotate Test Runner (Windows) ===

REM Check if Python is in the path
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found in PATH!
    echo Please install Python or add it to your PATH.
    exit /b 1
)

REM Check if the test script exists
if not exist run_tests.py (
    echo Error: run_tests.py not found!
    echo Please make sure you're running this from the project root.
    exit /b 1
)

REM Run the test automation script
python run_tests.py

REM Forward the exit code
exit /b %ERRORLEVEL%