# What's New in Version 0.6.0

## 🌟 New Features

### 📋 Configuration File Support

- **Multiple format support**: YAML (`.pyannotate.yaml`), JSON (`.pyannotate.json`), and TOML (`pyproject.toml`)
- **Project-specific settings**: Configure header metadata, ignored files/directories per project
- **Automatic discovery**: Config files are automatically found by walking up the directory tree
- **Backward compatible**: Works without config files (uses sensible defaults)
- **Header configuration**: Set author, email, version, date format (ready for future metadata features)
- **File filtering**: Extend ignored files and directories via configuration

**Example `.pyannotate.yaml`:**
```yaml
header:
  author: "Your Name"
  include_date: true
files:
  ignored_files: ["custom.txt"]
  ignored_directories: ["temp"]
```

**Note:** For YAML support, install `pyyaml`. For TOML on Python < 3.11, install `tomli`.

### 🔍 Dry-Run Mode

- **Preview changes before applying**: New `--dry-run` flag allows you to see what would be modified without actually changing files
- **Statistics summary**: Dry-run mode provides a summary of files that would be modified, skipped, or remain unchanged
- **Safe testing**: Perfect for reviewing changes before committing or testing configuration
- **Programmatic API**: Both `process_file()` and `walk_directory()` now support `dry_run` parameter
- **Enhanced logging**: Better visibility into what operations would be performed

**Usage:**
```bash
pyannotate --dry-run
```

**Python API:**
```python
from pyannotate.annotate_headers import walk_directory
stats = walk_directory(Path.cwd(), Path.cwd(), dry_run=True)
```

---

# What's New in Version 0.5.0

## 🌟 Critical Improvements

### 🚫 New IGNORED_FILES Set

- **Added comprehensive IGNORED_FILES set**: Files like `.prettierrc`, `.eslintrc`, `.babelrc`, and other configuration files are now properly ignored
- **Prevents breaking configuration files**: Avoids adding headers to files that shouldn't be modified (e.g., JSON config files without comment support)
- **Includes auto-generated files**: Lock files like `package-lock.json`, `yarn.lock`, `Pipfile.lock` are now skipped
- **IDE and system files**: Files like `.env.example`, IDE settings, and other system files are properly ignored

### 📝 Fixed Newline Handling

- **Eliminated unnecessary trailing newlines**: Files no longer get extra blank lines at the end
- **Improved content preservation**: Better handling of original file formatting
- **Smarter spacing**: Only adds blank lines between header and content when content exists and is non-empty

## 🔧 Technical Improvements

### Enhanced File Processing Logic

- **Smarter empty file detection**: Better handling of files with only whitespace
- **Improved shebang preservation**: More robust handling of script files with shebang lines
- **Better XML/HTML processing**: Enhanced handling of files with declarations while avoiding extra newlines

### Updated Exports

- **New constant available**: `IGNORED_FILES` is now exported from the package for external use
- **Version bump**: Updated to version 0.5.0 to reflect significant improvements

---

## What's New in Version 0.4.0

## 🌟 New Features and Improvements

### 🔄 Enhanced Header Detection and Handling

- **Smart Header Detection**: Now detects and adapts to various existing header formats
- **Format Preservation**: Merges existing header content with our standardized format
- **Meta Information Preservation**: Preserves author, copyright, and other metadata from existing headers

### 🌐 Expanded Web Framework Support

- **Vue.js Files**: Special handling for Vue Single File Components (SFCs)
- **Svelte Files**: Support for Svelte components
- **Astro Files**: Support for Astro framework files
- **React JSX/TSX**: Improved handling for React components

### 🧩 More File Types

- Added support for numerous additional file types:
  - **Markup & Documentation**: Extended support for reStructuredText (.rst)
  - **Programming Languages**: Enhanced support for Go, Rust, Zig, Elixir, Erlang, Haskell, Lisp, R, Julia
  - **Configuration**: Added various config file formats with appropriate comment styles

### 🔧 Technical Improvements in Version 0.4.0

- **Better Binary Detection**: Improved mechanism to identify binary files
- **DOCTYPE Preservation**: Better handling of HTML DOCTYPE declarations
- **Encoding Robustness**: Enhanced UTF-8 handling with graceful fallbacks

### 🚫 Skipped File Types

- Explicitly skips files that shouldn't be modified:
  - **Markdown (.md)**: Documentation files
  - **JSON (.json)**: Standard JSON files (only JSON5 is annotated)
  - **License files**: Files named "LICENSE" without extension
