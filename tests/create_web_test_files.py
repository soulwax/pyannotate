# File: tests/create_web_test_files.py

"""
Script to generate sample web framework files for testing.
Run this script to create a set of test files in tests/sample_web_files directory.
"""

from pathlib import Path

# Zentrale Templates & Erzeuger – vermeidet Duplikate in mehreren Dateien
from tests.helpers.components import create_web_framework_test_files


def create_test_files() -> Path:
    """Create all test files for web frameworks and return the base directory."""
    test_dir = Path("tests/sample_web_files")
    test_dir.mkdir(parents=True, exist_ok=True)

    # Erzeuge alle Framework-Dateien mithilfe des zentralen Helpers
    create_web_framework_test_files(test_dir)

    # Ausgabe der Struktur (dynamisch gelistet, kein statisches Mapping nötig)
    print(f"Test files created successfully in {test_dir}")
    print("Directory structure:")
    for path in sorted(test_dir.rglob("*")):
        rel = path.relative_to(test_dir)
        if path.is_dir():
            print(f"  {rel}/")
        else:
            print(f"    {rel.name}")

    return test_dir


if __name__ == "__main__":
    td = create_test_files()
    print(f"\nTo process these files, run: python -m annot8 -d {td}")
