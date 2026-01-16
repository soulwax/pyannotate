<!-- markdownlint-disable MD025 MD024 -->
# What's New in Version 0.10.0

## 🌟 Major Features

### 🔀 Git Integration

Comprehensive Git integration for seamless workflow integration:

- **Git-aware file processing**: 
  - `--git` flag: Process only files tracked by git
  - `--staged` flag: Process only files staged for commit (perfect for pre-commit hooks)
  - Automatic `.gitignore` respect (with optional `pathspec` library)
- **Git metadata extraction**:
  - `--use-git-metadata` flag: Automatically populate headers with git information
  - Author name from git config or file history
  - Email address from git config
  - Last modified date from git log
  - Config values take precedence over git metadata
- **Pre-commit hook support**:
  - `--install-hook` flag: Installs pre-commit hook to auto-annotate staged files
  - Hook automatically uses git metadata
  - Seamless integration with existing git workflows
- **Graceful fallbacks**: Works correctly even when git is unavailable

**Usage Examples:**

```bash
# Process only git-tracked files
pyannotate --git

# Process only staged files
pyannotate --staged

# Use git metadata in headers
pyannotate --use-git-metadata

# Combine: process staged files with git metadata
pyannotate --staged --use-git-metadata

# Install pre-commit hook
pyannotate --install-hook
```

**Python API:**

```python
from pyannotate.annotate_headers import walk_directory
from pyannotate.git_integration import get_git_metadata

# Process with git filtering
stats = walk_directory(
    project_root,
    project_root,
    git_mode="tracked",  # or "staged"
    use_git_metadata=True
)

# Get git metadata for a file
metadata = get_git_metadata(file_path, git_root)
```

**Note:** For full `.gitignore` support, install `pathspec`: `pip install pathspec`

---

# What's New in Version 0.9.1

## 🌟 Major Features

### 🔄 Revert Functionality

Added comprehensive revert functionality to undo changes made by PyAnnotate:

- **Automatic backup creation**: Backups are automatically created when files are modified
- **Manual revert**: Use `pyannotate --revert` to restore files to their state before the last run
- **Dry-run revert**: Preview revert operations with `pyannotate --revert --dry-run`
- **Backup file**: Backups are stored in `.pyannotate_backup.json` in the project root
- **Relative paths**: Backups use relative paths for portability across systems
- **Error handling**: Gracefully handles missing files, permission errors, and other edge cases

**Usage:**

```bash
# Normal annotation (creates backup automatically)
pyannotate

# Revert last changes
pyannotate --revert

# Preview revert without applying
pyannotate --revert --dry-run
```

**Python API:**

```python
from pyannotate.backup import revert_files
stats = revert_files(project_root, dry_run=False)
```

### 🎨 Shader File Protection

Added automatic protection for shader files that require `#version` directive at the top:

- **Supported shader types**: `.vert`, `.frag`, `.geom`, `.comp`, `.tesc`, `.tese`, `.glsl`, `.hlsl`, `.wgsl`, `.shader`
- **Automatic skipping**: Shader files are automatically skipped to prevent breaking compilation
- **Comprehensive coverage**: All common GLSL, HLSL, and WebGPU shader extensions are protected

**Reason**: Shader files must have `#version` as the first non-whitespace line; adding headers would break shader compilation.

## 🐛 Bug Fixes

- **Fixed test coverage**: Added missing `.tesc` and `.tese` extensions to shader extension tests for complete coverage

---

# What's New in Version 0.9.0

## 🌟 Major Features

### 🌐 Expanded Web Framework Support

Added support for **7 additional popular web templating frameworks**, bringing comprehensive coverage to modern web development:

**New Web Frameworks & Templating Languages:**

- **Handlebars** (`.hbs`, `.handlebars`) - `<!-- -->` comments
- **EJS** (`.ejs`) - `<!-- -->` comments (Embedded JavaScript)
- **Pug/Jade** (`.pug`, `.jade`) - `//` comments
- **Mustache** (`.mustache`, `.mst`) - `<!-- -->` comments
- **Twig** (`.twig`) - `{# #}` comments (PHP templating)
- **Jinja2** (`.jinja`, `.jinja2`) - `{# #}` comments (Python templating)
- **MDX** (`.mdx`) - `<!-- -->` comments (Markdown + JSX)

All new frameworks include:

- Proper comment style detection for each template language
- Special handling for template syntax preservation
- Comprehensive test coverage
- Sample files demonstrating usage

---

# What's New in Version 0.8.0

## 🌟 Major Features

### 🌐 Expanded Language Support

Added support for **18 additional programming languages**, bringing total support to **70+ languages and file formats**:

**New Languages Added:**

- **Objective-C** (`.m`, `.mm`) - `//` comments
- **Groovy** (`.groovy`) - `//` comments
- **Clojure** (`.clj`, `.cljs`, `.cljc`) - `;;` comments
- **F#** (`.fs`, `.fsx`, `.fsi`) - `//` comments
- **V** (`.v`) - `//` comments
- **Nim** (`.nim`) - `#` comments
- **Crystal** (`.cr`) - `#` comments
- **Nix** (`.nix`) - `#` comments
- **Terraform** (`.tf`, `.tfvars`) - `#` comments
- **HCL** (`.hcl`) - `#` comments
- **VHDL** (`.vhd`, `.vhdl`) - `--` comments
- **Ada** (`.adb`, `.ads`) - `--` comments
- **OCaml** (`.ml`, `.mli`) - `(* *)` comments
- **Pascal/Delphi** (`.pas`, `.pp`) - `//` comments
- **Assembly** (`.asm`, `.s`) - `;` comments
- **VB.NET** (`.vb`) - `'` comments
- **Fortran** (`.f`, `.f90`, `.f95`, `.f03`, `.f08`) - `!` comments
- **COBOL** (`.cob`, `.cbl`) - `*` comments

All new languages include comprehensive test coverage to ensure proper comment style detection and header processing.

### 🐛 Bug Fixes

- **Fixed multi-line template truncation**: Multi-line templates are now fully preserved when merging with existing headers instead of only using the first line
- **Improved header merging logic**: Templates with multiple lines now replace existing headers entirely, preserving the complete template structure

---

# What's New in Version 0.7.0

## 🌟 Major Features

### 🎨 Custom Header Templates

- **Full creative freedom**: Design your own header format with complete control
- **Variable substitution**: Use `{file_path}`, `{author}`, `{date}`, `{version}`, and more
- **Default values**: Use `{variable|default}` syntax for missing variables
- **Multi-line support**: Create complex multi-line headers with automatic comment formatting
- **File-specific variables**: Access `{file_name}`, `{file_stem}`, `{file_suffix}`, `{file_dir}`
- **Automatic formatting**: Each template line gets appropriate comment style for the file type

**Example:**

```yaml
header:
  template: |
    File: {file_path}
    Author: {author|Unknown}
    Date: {date}
    Version: {version|1.0.0}
```

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

# What's New in Version 0.6.0

## 🌟 New Features

### 🎨 Custom Header Templates

- **Full creative freedom**: Design your own header format with complete control
- **Variable substitution**: Use `{file_path}`, `{author}`, `{date}`, `{version}`, and more
- **Default values**: Use `{variable|default}` syntax for missing variables
- **Multi-line support**: Create complex multi-line headers with automatic comment formatting
- **File-specific variables**: Access `{file_name}`, `{file_stem}`, `{file_suffix}`, `{file_dir}`
- **Automatic formatting**: Each template line gets appropriate comment style for the file type

**Example:**

```yaml
header:
  template: |
    File: {file_path}
    Author: {author|Unknown}
    Date: {date}
    Version: {version|1.0.0}
```

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
