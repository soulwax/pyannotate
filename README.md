# PyAnnotate

📜 **A comprehensive Python tool** for automating the creation and maintenance of file headers across diverse programming languages and frameworks.

---

## 🌟 Key Features

- 🛠️ **Automatically updates and creates file headers** with intelligent detection and merging
- 🌐 **Supports 50+ programming languages and file formats**
- 🎨 **Advanced web framework support** (Vue, Svelte, Astro, React)
- 🔧 **Qt framework integration** (.pro, .ui, .ts translation files)
- 🔖 **Preserves special declarations** (shebang, DOCTYPE, XML declarations)
- 🧠 **Smart header detection and merging** - preserves existing metadata
- 🚫 **Intelligent file filtering** with comprehensive ignore patterns
- ⚙️ **Configuration-aware processing** with special handling for config files
- 🖥️ **CLI interface and Python API** for versatile usage
- 📝 **Robust text processing** with UTF-8 support and encoding fallbacks
- 🛡️ **Protects critical files** - automatically skips configs, lock files, and binaries

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

4. **Install development dependencies (for contributors):**

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

# Preview changes without modifying files (dry-run mode)
pyannotate --dry-run

# Combine options
pyannotate -d /path/to/project --dry-run -v
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

# Use dry-run mode to preview changes
from pyannotate.annotate_headers import process_file, walk_directory

# Preview changes for a single file
result = process_file(Path("example.py"), Path.cwd(), dry_run=True)
print(f"Status: {result['status']}")  # 'modified', 'skipped', or 'unchanged'

# Preview changes for entire directory
stats = walk_directory(Path.cwd(), Path.cwd(), dry_run=True)
print(f"Would modify: {stats['modified']} files")
print(f"Would skip: {stats['skipped']} files")
print(f"Unchanged: {stats['unchanged']} files")
```
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
read_file

---

## 📁 Comprehensive File Support

PyAnnotate automatically recognizes a vast array of file types and applies appropriate comment styles:

### 🐍 **Programming Languages**

| Language | Extensions | Comment Style |
|----------|------------|---------------|
| **Python** | `.py` | `#` |
| **JavaScript/TypeScript** | `.js`, `.ts`, `.jsx`, `.tsx` | `//` |
| **C/C++/C#** | `.c`, `.cpp`, `.h`, `.hpp`, `.cs` | `//` |
| **Java** | `.java` | `//` |
| **Go** | `.go` | `//` |
| **Rust** | `.rs` | `//` |
| **Swift** | `.swift` | `//` |
| **Kotlin** | `.kt` | `//` |
| **Scala** | `.scala` | `//` |
| **Zig** | `.zig` | `//` |
| **Dart** | `.dart` | `//` |
| **PHP** | `.php` | `//` |

### 🔧 **Systems & Scripting**

| Category | Extensions | Comment Style |
|----------|------------|---------------|
| **Shell Scripts** | `.sh`, `.bash`, `.zsh`, `.fish` | `#` |
| **PowerShell** | `.ps1`, `.psm1`, `.psd1` | `#` |
| **Batch Files** | `.cmd`, `.bat` | `REM` |
| **Ruby** | `.rb` | `#` |
| **Perl** | `.pl`, `.pm` | `#` |
| **Lua** | `.lua` | `--` |
| **Tcl** | `.tcl` | `#` |

### 🧮 **Functional & Data Science**

| Category | Extensions | Comment Style |
|----------|------------|---------------|
| **Haskell** | `.hs` | `--` |
| **Lisp Family** | `.lisp`, `.cl`, `.el` | `;;` |
| **Elixir** | `.ex`, `.exs` | `#` |
| **Erlang** | `.erl`, `.hrl` | `%` |
| **R** | `.r`, `.R` | `#` |
| **Julia** | `.jl` | `#` |

### 🌐 **Web Technologies**

| Category | Extensions | Comment Style | Special Handling |
|----------|------------|---------------|------------------|
| **HTML/XML** | `.html`, `.htm`, `.xml` | `<!-- -->` | Preserves DOCTYPE |
| **CSS/Styling** | `.css`, `.scss`, `.sass`, `.less` | `/* */` | - |
| **Vue.js** | `.vue` | `<!-- -->` | Template preservation |
| **Svelte** | `.svelte` | `<!-- -->` | Component structure |
| **Astro** | `.astro` | `<!-- -->` | Frontmatter preservation |
| **React JSX/TSX** | `.jsx`, `.tsx` | `//` | - |

### 🔧 **Configuration & Data**

| Category | Extensions | Comment Style |
|----------|------------|---------------|
| **YAML** | `.yaml`, `.yml` | `#` |
| **TOML** | `.toml` | `#` |
| **INI/Config** | `.ini`, `.conf`, `.cfg` | `#` |
| **Properties** | `.properties` | `#` |
| **JSON5** | `.json5` | `//` |
| **SQL** | `.sql` | `--` |
| **reStructuredText** | `.rst` | `..` |

### 🎨 **Qt Framework**

| File Type | Extensions | Comment Style | Special Features |
|-----------|------------|---------------|------------------|
| **Project Files** | `.pro`, `.pri` | `#` | - |
| **UI Files** | `.ui` | `<!-- -->` | XML declaration preservation |
| **Resource Files** | `.qrc` | `<!-- -->` | - |
| **Translation Files** | `.ts` | `<!-- -->` | Auto-detects vs TypeScript |

### 📋 **Special Configuration Files**

PyAnnotate intelligently handles configuration files with appropriate comment styles:

- **Git**: `.gitignore`, `.gitattributes`, `.gitmodules`
- **Docker**: `Dockerfile`, `docker-compose.yml`
- **Build Systems**: `Makefile`, `CMakeLists.txt`
- **Package Managers**: `Pipfile`, `pyproject.toml`, `setup.py`
- **CI/CD**: `.travis.yml`, `.gitlab-ci.yml`, `.drone.yml`
- **JavaScript Ecosystem**: `package.json`, `tsconfig.json`, `webpack.config.js`
- **And many more...**

---

## 🚫 Protected Files & Directories

### 🔒 **Completely Ignored Files**

PyAnnotate automatically skips files that shouldn't be modified:

#### Configuration Files

- **Linting/Formatting**: `.prettierrc`, `.eslintrc`, `.babelrc`, `.stylelintrc`
- **Build Tools**: `.browserslistrc`, `.nvmrc`, `.npmrc`, `.yarnrc`
- **Environment**: `.env.example`, `.env.local`, `.env.development`, `.env.production`

#### Auto-Generated Files

- **Lock Files**: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Pipfile.lock`, `poetry.lock`, `Cargo.lock`, `go.sum`
- **Build Artifacts**: Files in `build/`, `dist/`, `.next/`, `.nuxt/`, `coverage/`

#### Documentation & Legal

- **License Files**: `LICENSE`, `COPYING`, `NOTICE`, `AUTHORS`, `CONTRIBUTORS`
- **Documentation**: `README.md`, `CHANGELOG.md` (Markdown files)
- **Standard JSON**: `.json` files (only JSON5 gets headers)

#### Binary Files

- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.ico`, `.webp`
- **Audio/Video**: `.mp3`, `.mp4`, `.wav`, `.avi`
- **Archives**: `.zip`, `.tar`, `.gz`, `.7z`
- **Executables**: `.exe`, `.dll`, `.so`, `.bin`
- **And many more binary formats...**

### 📁 **Ignored Directories**

- **Build/Cache**: `__pycache__`, `node_modules`, `build`, `dist`, `.cache`
- **Version Control**: `.git`, `.hg`, `.svn`
- **Virtual Environments**: `venv`, `.venv`
- **Modern Build Tools**: `.next`, `.nuxt`, `.output`, `.parcel-cache`
- **Package Managers**: `.yarn`, `.pnpm-store`, `vendor`, `bower_components`

---

## 🎯 Advanced Features

### 🔍 **Dry-Run Mode**

Preview changes before applying them! Use `--dry-run` to see what would be modified without actually changing any files:

```bash
pyannotate --dry-run
```

**Output includes:**
- List of files that would be modified
- Summary statistics (modified, skipped, unchanged counts)
- Safe preview of all changes

This is especially useful for:
- Reviewing changes before committing
- Understanding the scope of modifications
- Testing configuration changes
- CI/CD pipelines for validation

### 🧠 **Intelligent Header Processing**

- **Header Detection**: Recognizes various existing header formats (`# File:`, `// Filename:`, `@file`, etc.)
- **Smart Merging**: Preserves valuable metadata (author, version, copyright) while standardizing format
- **Duplicate Prevention**: Prevents duplicate headers on repeated processing

### 🔧 **Special Declaration Handling**

- **Shebang Preservation**: Keeps `#!/bin/bash` and similar at the very top
- **XML Declarations**: Preserves `<?xml version="1.0"?>` and `<!DOCTYPE>` declarations
- **Web Framework Structures**: Maintains `<template>`, `<script setup>`, and frontmatter positioning

### 🌐 **Web Framework Intelligence**

- **Vue.js**: Proper handling of Single File Components with `<template>`, `<script>`, `<style>` sections
- **Svelte**: Component structure preservation
- **Astro**: Frontmatter and component boundary respect
- **React**: JSX/TSX with proper import preservation

### 🎨 **Qt Framework Integration**

- **Project Files**: Handles Qt `.pro` and `.pri` files with proper comment syntax
- **UI Files**: XML-based `.ui` files with declaration preservation  
- **Translation Files**: Intelligent detection between Qt `.ts` translation files and TypeScript files
- **Resource Files**: `.qrc` XML resource files

### 🔄 **Robust Text Processing**

- **UTF-8 Support**: Primary UTF-8 processing with graceful fallback encoding
- **Newline Normalization**: Consistent newline handling without unnecessary trailing lines
- **Binary Detection**: Content-based binary file detection beyond just extensions
- **Whitespace Intelligence**: Smart handling of empty files and whitespace-only content

---

## ⚙️ **Configuration & Customization**

### 🛠️ **Extending File Support**

```python
from pyannotate import PATTERNS, FilePattern

# Add custom file types
PATTERNS.append(FilePattern([".custom"], "//", ""))

# Add multi-line comment style
PATTERNS.append(FilePattern([".special"], "/*", "*/"))
```

### 🚫 **Customizing Ignored Items**

```python
from pyannotate import IGNORED_DIRS, IGNORED_FILES, SPECIAL_FILE_COMMENTS

# Extend ignored directories
IGNORED_DIRS.add("my_custom_build_dir")

# Add files to completely ignore
IGNORED_FILES.add("my-config.json")

# Define special files with unique comment styles
SPECIAL_FILE_COMMENTS["my-config"] = ("#", "")
```

### 🎯 **Advanced Pattern Configuration**

```python
# Access all available constants
from pyannotate import (
    PATTERNS,           # File extension patterns and comment styles
    IGNORED_DIRS,       # Directories to skip during traversal
    IGNORED_FILES,      # Files to completely ignore
    BINARY_EXTENSIONS,  # Known binary file extensions
    SPECIAL_FILE_COMMENTS  # Special files with custom comment styles
)
```

---

## 🆕 **What's New in Version 0.5.0**

### 🚫 **Enhanced File Protection**

- **Comprehensive IGNORED_FILES set**: Automatically skips 40+ configuration and system files
- **Prevents configuration breakage**: Files like `.prettierrc`, `.eslintrc`, `.babelrc` are safely ignored
- **Lock file protection**: Auto-generated files like `package-lock.json`, `yarn.lock` won't be modified
- **Environment file safety**: All `.env.*` variants are properly protected

### 📝 **Improved Text Processing**

- **Eliminated trailing newlines**: Files no longer get unnecessary blank lines at the end
- **Smarter spacing logic**: Only adds blank lines between header and content when appropriate
- **Better empty file handling**: Enhanced processing of files with only whitespace
- **Preserved content integrity**: More robust handling of original file formatting

### 🔧 **Technical Improvements**

- **Enhanced binary detection**: Better identification of binary files to skip
- **UTF-8 robustness**: Improved encoding handling with graceful fallbacks
- **Processing efficiency**: Optimized file processing logic with fewer unnecessary writes

---

## 🤝 **Contributing**

**Contributions to PyAnnotate are welcome!** Please open a Pull Request for any improvements.

### 🚀 **Development Setup**

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/soulwax/pyannotate.git
   cd pyannotate
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate    # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run the test suite:**

   ```bash
   # Run all tests with coverage
   pytest --cov=pyannotate tests/
   
   # Run linting
   pylint src/pyannotate tests
   
   # Format code
   black .
   
   # All-in-one command
   make check
   ```

### 🧪 **Testing Coverage**

The project maintains comprehensive test coverage including:

- **Core functionality**: File processing, header detection, merging
- **Web frameworks**: Vue, Svelte, Astro, React component handling  
- **Qt integration**: Project files, UI files, translation file detection
- **Special cases**: Shebang preservation, XML declarations, UTF-8 handling
- **Error conditions**: Binary files, encoding issues, permission problems

---

## 🔮 **Roadmap & Future Enhancements**

### 🚧 **Planned Features**

- [ ] **Configuration files**: YAML/JSON config for project-specific settings
- [ ] **Custom templates**: Configurable header templates with variables
- [ ] **Metadata insertion**: Automatic author/date/version information
- [ ] **Git integration**: Pre-commit hooks and Git-aware processing
- [x] **Dry-run mode**: Preview changes before applying
- [ ] **Rollback functionality**: Undo header additions

### 🌐 **Language Expansion**

- [ ] **Additional frameworks**: Support for more web and mobile frameworks
- [ ] **Domain-specific formats**: CAD files, scientific data formats
- [ ] **Template engines**: Jinja2, Handlebars, Mustache templates

### 🛠️ **Tooling Improvements**

- [ ] **IDE integrations**: VS Code, IntelliJ plugins
- [ ] **CI/CD actions**: GitHub Actions, GitLab CI templates
- [ ] **GUI interface**: Desktop application for non-technical users
- [ ] **Web dashboard**: Browser-based project management

### 📦 **Distribution**

- [ ] **PyPI publication**: Official package distribution
- [ ] **Docker containers**: Containerized execution environments
- [ ] **Package managers**: Homebrew, Scoop, APT packages

---

## 📜 **License**

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for complete details.

---

## 🙏 **Acknowledgments**

PyAnnotate supports the development workflows of programmers across dozens of languages and frameworks. Special recognition for comprehensive support of:

- **Web Development**: Vue.js, Svelte, Astro, React ecosystems
- **Systems Programming**: Rust, Go, Zig, and C/C++ development
- **Cross-Platform Development**: Qt framework integration
- **DevOps & Configuration**: Extensive config file format support
- **Data Science**: R, Julia, and Python scientific computing workflows

---

*Streamline your project's header management with PyAnnotate - because consistent code documentation shouldn't be a manual chore.*
