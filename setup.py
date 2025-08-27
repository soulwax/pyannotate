# File: setup.py

from setuptools import find_packages, setup

# Read README with explicit UTF-8 encoding
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="pyannotate",
    version="0.4.0",  # Incremented version for new features
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pyannotate=pyannotate.cli:main",
        ],
    },
    author="soulwax",
    author_email="soulwax@nandcore.com",
    description="Python package to annotate files with headers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soulwax/pyannotate",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",  # Added Python 3.13 support
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)
