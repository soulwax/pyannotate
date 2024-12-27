# PyAnnotate

📜 **A soon to be truly powerful Python tool** for automating the creation and maintenance of file headers in projects.

---

## 🌟 Key Features

- 🛠️ **Automatically updates and creates file headers**
- 🌐 **Supports numerous programming languages and file types**
- 🔖 **Preserves shebang lines** in scripts
- 🚫 **Customizable exclude directories**
- ⚙️ **Specific handling of configuration files**
- 🖥️ **CLI interface and Python API for versatile usage**

---

## 🛠️ Installation

While the package is pending on PyPi you cannot install it via `pip install PyAnnotate`, you can install it locally instead:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/soulwax/pyannotate.git
   cd pyannotate
   ```

2. **Install in editable mode:**

   ```bash
   pip install -e .
   ```

3. **Install development dependencies:**

   ```bash
   pip install -r requirements-dev.txt
   ```

---

## 🚀 Usage

### 🖥️ **Command-Line Interface**

After installation, the `pyannotate` command is available:

```bash
# Annotate files in the current directory
pyannotate

# Annotate files in a specific directory
pyannotate -d /path/to/project

# Enable verbose logging
pyannotate -v
```

### 🐍 **Python API**

For use in Python scripts:

```python
from pathlib import Path
from pyannotate import process_file, walk_directory

# Process a single file
process_file(Path("example.py"), Path.cwd())

# Process an entire directory
walk_directory(Path.cwd(), Path.cwd())
```

---

## Supported File Types

PyAnnotate automatically recognizes various file types and applies the appropriate comment styles:

- **Python** (.py): `#`
- **JavaScript/TypeScript** (.js, .ts, .jsx, .tsx): `//`
- **CSS** (.css): `/* */`
- **HTML/XML** (.html, .xml, .svg): `<!-- -->`
- **Shell scripts** (.sh, .bash): `#`
- **C/C++** (.c, .cpp, .h, .hpp): `//`
- **Markdown** (.md): `<!-- -->`
- **And many more formats...**

---

## ⚙️ Configuration Options

PyAnnotate automatically detects most common file types but also offers flexible customization options. Changes can be made by modifying the following constants:

```python
from pyannotate import PATTERNS, IGNORED_DIRS, CONFIG_FILES

# Add custom file types
PATTERNS.append(FilePattern([".custom"], "//"))

# Extend ignored directories
IGNORED_DIRS.add("custom_modules")

# Define specific configuration files
CONFIG_FILES[".customrc"] = "//"
```

---

## 🔮 (Possible) Future Enhancements

### 🚧 Planned Features

- [ ] Add support for multi-line comment styles (e.g., `/* */` for CSS)
- [ ] Implement configuration file support (YAML/JSON) for project-specific settings
- [ ] Add option to customize header template
- [ ] Create option to add author/date information to headers
- [ ] Develop pre-commit hook integration

### 🌐 Language and File Type Expansion

- [ ] Add more file type support (Ruby, Go, Rust, etc.)
- [ ] Improve handling of complex comment styles
- [ ] Better support for configuration and build files

### 🛠️ Improvements

- [ ] Add dry-run mode to preview changes
- [ ] Implement rollback/undo functionality
- [ ] Create more comprehensive logging options
- [ ] Add unit tests for edge cases
- [ ] Develop GUI or web interface for configuration

### 🔒 Robustness and Performance

- [ ] Optimize file processing for large projects
- [ ] Add more robust error handling
- [ ] Implement file change tracking to minimize unnecessary writes
- [ ] Create performance benchmarking tools

### 📦 Packaging and Distribution

- [ ] Publish package to PyPI
- [ ] Create Docker container for easy deployment
- [ ] Develop GitHub Action for automatic header maintenance

---

## 🤝 Contributing

**Contributions to PyAnnotate are welcome!** Please open a Pull Request. For major changes, we recommend creating an issue first.

1. **Fork the repository:**

   ```bash
   git clone https://github.com/soulwax/pyannotate.git
   ```

2. **Create a feature branch:**

   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Install development dependencies:**

   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Make your changes.**
5. **Run tests:**

   ```bash
   pytest
   ```

6. **Check linting:**

   ```bash
   pylint src/pyannotate tests
   ```

7. **Commit your changes:**

   ```bash
   git commit -m 'Add amazing feature'
   ```

8. **Push to the branch:**

   ```bash
   git push origin feature/AmazingFeature
   ```

9. **Open a Pull Request.**

---

## 📜 License

This project is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](LICENSE) file.
