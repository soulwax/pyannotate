# What's New in Version 0.4.0

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

### 🔧 Technical Improvements

- **Better Binary Detection**: Improved mechanism to identify binary files
- **DOCTYPE Preservation**: Better handling of HTML DOCTYPE declarations
- **Encoding Robustness**: Enhanced UTF-8 handling with graceful fallbacks

### 🚫 Skipped File Types

- Explicitly skips files that shouldn't be modified:
  - **Markdown (.md)**: Documentation files
  - **JSON (.json)**: Standard JSON files (only JSON5 is annotated)
  - **License files**: Files named "LICENSE" without extension
