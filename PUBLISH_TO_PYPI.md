# Publishing to PyPI Guide

This guide will walk you through publishing your LLM Regression Tester package to PyPI (Python Package Index) so others can install it with `pip install llm-regression-tester`.

## Prerequisites

1. **PyPI Account**: Create a free account at [https://pypi.org/](https://pypi.org/)
2. **Test PyPI Account**: Also create an account at [https://test.pypi.org/](https://test.pypi.org/) for testing
3. **Build Tools**: Install the build package
   ```bash
   pip install build
   ```
4. **Publishing Tool**: Install Twine
   ```bash
   pip install twine
   ```

## Step 1: Prepare Your Package

### Update Version Number

Before publishing, update the version in these files:
- `pyproject.toml` (line 7)
- `src/llm_regression_tester/_version.py` (line 3)

Increment according to [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., 0.1.0 → 0.1.1 for bug fixes)

### Update Metadata

Ensure your `pyproject.toml` has accurate information:
- Author name and email
- Description
- Keywords
- URLs (Homepage, Repository, etc.)

### Build Your Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build both source distribution and wheel
python -m build
```

This creates:
- `dist/llm_regression_tester-X.Y.Z.tar.gz` (source distribution)
- `dist/llm_regression_tester-X.Y.Z-py3-none-any.whl` (wheel)

## Step 2: Test Your Package

### Test Installation Locally

```bash
# Install from wheel
pip install dist/llm_regression_tester-X.Y.Z-py3-none-any.whl

# Test import
python -c "import llm_regression_tester; print('Success!')"
```

### Upload to Test PyPI

```bash
# Upload to Test PyPI (safe testing environment)
twine upload --repository testpypi dist/*

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ llm-regression-tester

# Test that it works
python -c "import llm_regression_tester; print(llm_regression_tester.__version__)"
```

## Step 3: Publish to Production PyPI

### Final Checks

1. ✅ All tests pass: `pytest`
2. ✅ Package builds successfully: `python -m build`
3. ✅ Package installs correctly from wheel
4. ✅ Documentation is complete and accurate
5. ✅ Version number is updated
6. ✅ CHANGELOG.md is updated with new version

### Upload to Production PyPI

```bash
# Upload to production PyPI (real deal!)
twine upload dist/*
```

**Important**: This command uploads to the real PyPI. Once uploaded, you cannot change or delete the package. Make sure everything is perfect!

## Step 4: Post-Publishing

### Verify Installation

```bash
# Test that others can install it
pip install llm-regression-tester

# Verify it works
python -c "import llm_regression_tester; print(f'Version: {llm_regression_tester.__version__}')"
```

### Update GitHub Repository

```bash
# Tag the release
git tag v0.1.0
git push origin v0.1.0

# Create a GitHub release with the changelog
# Go to: https://github.com/ktech99/llm-regression-tester/releases
# Click "Create a new release"
# Tag: v0.1.0
# Title: Version 0.1.0
# Description: Copy from CHANGELOG.md
```

### Update Documentation

- Update any README badges to point to the new PyPI version
- Ensure installation instructions work
- Add a "PyPI" badge to your README

## Common Issues and Solutions

### Authentication Issues
If you get authentication errors:
```bash
# Create ~/.pypirc file
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...

[testpypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```

### Build Errors
If builds fail:
```bash
# Clean everything
rm -rf dist/ build/ *.egg-info/ src/*.egg-info/

# Rebuild
python -m build
```

### Import Errors
If imports fail after installation:
- Check your `src/` directory structure
- Ensure `__init__.py` files exist
- Verify package name in `pyproject.toml` matches your import name

## Maintenance

### Updating Your Package

1. Make your changes
2. Update version number
3. Update CHANGELOG.md
4. Build and test
5. Publish to PyPI
6. Tag and release on GitHub

### Monitoring Downloads

Check your package stats at:
- [https://pypi.org/project/llm-regression-tester/](https://pypi.org/project/llm-regression-tester/)
- [https://pepy.tech/project/llm-regression-tester](https://pepy.tech/project/llm-regression-tester)

## Security Best Practices

1. **Never commit API keys** - Use `.env` files (already in `.gitignore`)
2. **Use HTTPS** for all PyPI operations
3. **Enable 2FA** on your PyPI account
4. **Review dependencies** regularly for security updates
5. **Test thoroughly** before publishing to production

## Support

If you encounter issues:
1. Check the [PyPI help documentation](https://pypi.org/help/)
2. Search existing GitHub issues
3. Create a new issue with detailed error messages

---

🎉 **Congratulations!** Your package is now available on PyPI for the world to use!
