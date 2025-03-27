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

2. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install in editable mode:**

   ```bash
   pip install -e .
   ```

4. Install development dependencies (when contributing):

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
- **And many more formats... e.g.:**
--**JSON5** (.json5): `//`
--**TOML** (.toml): `#`

Suffice to say there is more to come.

## File formats we leave alone

- **Markdown** (.md): `<!-- -->`
- **JSON** (.json): `//`

---

## ⚙️ Configuration Options

PyAnnotate automatically detects most common file types but also offers flexible customization options. Changes can be made by modifying the following constants:

```python
from pyannotate import PATTERNS, IGNORED_DIRS, SPECIAL_FILE_COMMENTS

# Add custom file types
PATTERNS.append(FilePattern([".custom"], "//"))

# Extend ignored directories
IGNORED_DIRS.add("custom_modules")

# Define specific files with unique comment styles (e.g., `.customrc`)
SPECIAL_FILE_COMMENTS[".customrc"] = "//"
```

---

## 🔮 (Possible) Future Enhancements

### 🚧 Planned Features

- [x] Add support for multi-line comment styles (e.g., `/* */` for CSS)
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

3. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate    # On Windows
   ```

4. **Install dependencies:**

   ```bash
   # First install required dependencies
   pip install -r requirements.txt
   
   # Then install development dependencies
   pip install -r requirements-dev.txt
   ```

5. **Make your changes.**
6. **Run tests:**

   ```bash
   pytest
   ```

7. **Check linting:**

   ```bash
   pylint src/pyannotate tests
   ```

   All in one:

      ```bash
      black . && pylint src/pyannotate tests > pylint.txt ; pytest --cov=pyannotate tests/ > pytest.txt
      ```

   This will run the tests, check the code style, and generate coverage reports. Make sure all tests pass and coverage is maintained, and the score is 10.00/10.00.

8. **Commit your changes:**

   ```bash
   git commit -m 'Add amazing feature'
   ```

9. **Push to the branch:**

   ```bash
   git push origin feature/AmazingFeature
   ```

10. **Open a Pull Request.**

---

## 📜 License

This project is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](LICENSE) file.
