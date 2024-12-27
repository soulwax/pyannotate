# PyAnnotate

A Python tool for automatically adding and maintaining file headers across your project.

## Features

- Automatically adds and updates file headers
- Supports multiple programming languages and file types
- Preserves shebang lines in scripts
- Configurable ignored directories
- Special handling for configuration files
- Command-line interface and Python API

## Installation

```bash
pip install pyannotate
```

## Usage

### Command Line Interface

```bash
# Annotate files in current directory
pyannotate

# Annotate files in specific directory
pyannotate -d /path/to/project

# Enable verbose logging
pyannotate -v
```

### Python API

```python
from pathlib import Path
from pyannotate import process_file, walk_directory

# Process a single file
process_file(Path("example.py"), Path.cwd())

# Process entire directory
walk_directory(Path.cwd(), Path.cwd())
```

## Supported File Types

PyAnnotate supports various file types with appropriate comment styles:

- Python (.py): `#`
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx): `//`
- CSS (.css): `/* */`
- HTML/XML (.html, .xml, .svg): `<!-- -->`
- Shell scripts (.sh, .bash): `#`
- C/C++ (.c, .cpp, .h, .hpp): `//`
- Markdown (.md): `<!-- -->`
- And many more...

## Configuration

PyAnnotate automatically detects file types and applies appropriate comment styles. You can customize the behavior by modifying the following constants in your code:

```python
from pyannotate import PATTERNS, IGNORED_DIRS, CONFIG_FILES

# Add custom file patterns
PATTERNS.append(FilePattern([".custom"], "//"))

# Modify ignored directories
IGNORED_DIRS.add("custom_modules")

# Add special configuration files
CONFIG_FILES[".customrc"] = "//"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Install development dependencies (`pip install -r requirements-dev.txt`)
4. Make your changes
5. Run tests (`pytest`)
6. Run linting (`pylint src/pyannotate tests`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/AmazingFeature`)
9. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
