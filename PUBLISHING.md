# Publishing Guide for PyAnnotate

This guide explains how to publish PyAnnotate to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account on [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)
2. **GitHub Secrets**: Set up the following secrets in your GitHub repository:
   - `PYPI_API_TOKEN` - API token for PyPI (for trusted publishing, use OIDC)
   - `TEST_PYPI_API_TOKEN` - API token for TestPyPI (optional, for testing)

## Publishing Methods

### Method 1: Automated Publishing via GitHub Release (Recommended)

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "0.11.0"
   ```

2. **Update CHANGELOG.md** with the new version's changes

3. **Commit and push** the changes:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to 0.11.0"
   git push
   ```

4. **Create a GitHub release**:
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Tag: `v0.11.0` (must match version in pyproject.toml)
   - Title: `Version 0.11.0`
   - Description: Copy from CHANGELOG.md
   - Click "Publish release"

5. **GitHub Actions will automatically**:
   - Build the package
   - Check the package with `twine check`
   - Publish to PyPI

### Method 2: Manual Publishing via GitHub Actions

1. Go to "Actions" → "Publish to PyPI" → "Run workflow"
2. Fill in:
   - Version: `0.11.0`
   - Test PyPI: `false` (or `true` to test first)
3. Click "Run workflow"

### Method 3: Local Publishing (for testing)

1. **Install build tools**:
   ```bash
   pip install build twine
   ```

2. **Build the package**:
   ```bash
   python -m build
   ```

3. **Check the package**:
   ```bash
   twine check dist/*
   ```

4. **Upload to TestPyPI** (for testing):
   ```bash
   twine upload --repository testpypi dist/*
   ```

5. **Test installation from TestPyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ pyannotate
   ```

6. **Upload to PyPI** (when ready):
   ```bash
   twine upload dist/*
   ```

## Version Management

- Use [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`
- Update version in `pyproject.toml`
- Update `CHANGELOG.md` with new features/changes
- Create a git tag: `git tag v0.11.0 && git push --tags`

## Optional Dependencies

The package supports optional dependencies via extras:

- `yaml`: For YAML configuration file support (`pyyaml>=6.0`)
- `gitignore`: For full `.gitignore` support (`pathspec>=0.10.3`)
- `toml`: For TOML support on Python < 3.11 (`tomli>=2.0.0`)

Users can install with:
```bash
pip install pyannotate[yaml,gitignore,toml]
```

## Troubleshooting

### Build fails
- Ensure `pyproject.toml` is valid TOML
- Check that all required fields are present
- Verify `MANIFEST.in` includes necessary files

### Upload fails
- Verify PyPI credentials are correct
- Check that the version doesn't already exist on PyPI
- Ensure package name is available

### TestPyPI vs PyPI
- TestPyPI is for testing package builds
- PyPI is the production package index
- You can upload the same version to both (for testing)

## Post-Publication

1. **Verify installation**:
   ```bash
   pip install pyannotate
   pyannotate --help
   ```

2. **Update README** if needed (installation instructions should already be updated)

3. **Announce the release** on:
   - GitHub Releases
   - Project documentation
   - Social media (if applicable)
