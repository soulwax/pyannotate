# PyAnnotate

📜 **A powerful Python tool** for automating the creation and maintenance of file headers in projects.

---

## 🌟 Key Features

- 🛠️ **Automatically updates and creates file headers**
- 🌐 **Supports numerous programming languages and file types**
- 🔖 **Preserves shebang lines** in scripts
- 🚫 **Smart file filtering** with customizable exclude directories and ignored files
- ⚙️ **Specific handling of configuration files**
- 🖥️ **CLI interface and Python API for versatile usage**
- 📝 **Improved newline handling** - no more unnecessary trailing newlines
- 🛡️ **Protects configuration files** - automatically skips files like `.prettierrc`, `.eslintrc`, etc.

---

## 🛠️ Installation

While the package is pending on PyPI, you can install it locally:

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
- **HTML/XML** (.html, .xml): `<!-- -->`
- **Shell scripts** (.sh, .bash): `#`
- **C/C++** (.c, .cpp, .h, .hpp): `//`
- **Vue/Svelte/Astro** (.vue, .svelte, .astro): `<!-- -->`
- **And many more formats... e.g.:**
  - **JSON5** (.json5): `//`
  - **TOML** (.toml): `#`
  - **Go** (.go): `//`
  - **Rust** (.rs): `//`
  - **Ruby** (.rb): `#`

---

## File Formats We Leave Alone

### 🚫 Completely Ignored Files

- **Configuration files**: `.prettierrc`, `.eslintrc`, `.babelrc`, `.stylelintrc`
- **Lock files**: `package-lock.json`, `yarn.lock`, `Pipfile.lock`, `poetry.lock`
- **Environment files**: `.env.example`, `.env.local`, `.env.development`, `.env.production`
- **License files**: `LICENSE`, `COPYING`, `NOTICE`, `AUTHORS`
- **Auto-generated files**: Various build and cache files

### 📝 Skipped for Headers

- **Markdown** (.md, .markdown): Documentation files
- **JSON** (.json): Standard JSON files (only JSON5 gets headers)

---

## ⚙️ Configuration Options

PyAnnotate automatically detects most common file types and offers flexible customization:

```python
from pyannotate import PATTERNS, IGNORED_DIRS, IGNORED_FILES, SPECIAL_FILE_COMMENTS

# Add custom file types
PATTERNS.append(FilePattern([".custom"], "//"))

# Extend ignored directories
IGNORED_DIRS.add("custom_modules")

# Add files to ignore completely
IGNORED_FILES.add("custom-config.json")

# Define specific files with unique comment styles
SPECIAL_FILE_COMMENTS[".customrc"] = ("#", "")
```

---

## 🆕 What's New in Version 0.5.0

### 🚫 Smart File Filtering

- **New IGNORED_FILES set**: Automatically skips configuration files that shouldn't have headers
- **Prevents breaking configs**: Files like `.prettierrc`, `.eslintrc`, `.babelrc` are now safely ignored
- **Protects lock files**: Auto-generated files like `package-lock.json`, `yarn.lock` won't be modified

### 📝 Improved Output Quality  

- **No more trailing newlines**: Files no longer get unnecessary blank lines at the end
- **Better spacing**: Smarter handling of blank lines between headers and content
- **Cleaner processing**: Enhanced handling of empty files and whitespace-only files

---

## 🔮 Future Enhancements

### 🚧 Planned Features

- [ ] Implement configuration file support (YAML/JSON) for project-specific settings
- [ ] Add option to customize header template
- [ ] Create option to add author/date information to headers
- [ ] Develop pre-commit hook integration
- [ ] Add dry-run mode to preview changes
- [ ] Implement rollback/undo functionality

### 🌐 Language and File Type Expansion

- [ ] Add more specialized file type support
- [ ] Improve handling of complex comment styles
- [ ] Better support for domain-specific configuration files

### 🛠️ Improvements

- [ ] Create more comprehensive logging options
- [ ] Develop GUI or web interface for configuration
- [ ] Add unit tests for edge cases
- [ ] Implement file change tracking to minimize unnecessary writes

### 🔒 Robustness and Performance

- [ ] Optimize file processing for large projects
- [ ] Add more robust error handling
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
