#!/usr/bin/env python3
"""
Pre-publishing checklist for LLM Regression Tester.

This script verifies that everything is ready for publishing:
- Version consistency
- Package metadata
- Required files
- Test coverage
- Documentation

Usage:
    python pre_publish_checklist.py
"""

import json
import re
from pathlib import Path
import sys

def check_version_consistency():
    """Check that version is consistent across all files."""
    print("🔍 Checking version consistency...")

    # Read version from pyproject.toml
    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.exists():
        print("   ❌ pyproject.toml not found")
        return False

    with open(pyproject_path, 'r') as f:
        content = f.read()
        pyproject_match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if not pyproject_match:
            print("   ❌ Version not found in pyproject.toml")
            return False
        pyproject_version = pyproject_match.group(1)

    # Read version from _version.py
    version_path = Path('src/llm_regression_tester/_version.py')
    if not version_path.exists():
        print("   ❌ _version.py not found")
        return False

    with open(version_path, 'r') as f:
        content = f.read()
        version_match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
        if not version_match:
            print("   ❌ Version not found in _version.py")
            return False
        version_py_version = version_match.group(1)

    if pyproject_version != version_py_version:
        print(f"   ❌ Version mismatch: pyproject.toml={pyproject_version}, _version.py={version_py_version}")
        return False

    print(f"   ✅ Version {pyproject_version} is consistent")
    return True

def check_required_files():
    """Check that all required files are present."""
    print("\n🔍 Checking required files...")

    required_files = [
        'README.md',
        'LICENSE',
        'pyproject.toml',
        'src/llm_regression_tester/__init__.py',
        'src/llm_regression_tester/llm_regression_tester.py',
        'src/llm_regression_tester/_version.py',
        'tests/test_basic.py'
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"   ❌ Missing required files: {missing_files}")
        return False

    print("   ✅ All required files are present")
    return True

def check_package_metadata():
    """Check package metadata in pyproject.toml."""
    print("\n🔍 Checking package metadata...")

    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.exists():
        print("   ❌ pyproject.toml not found")
        return False

    with open(pyproject_path, 'r') as f:
        content = f.read()

    required_fields = [
        'name',
        'version',
        'description',
        'authors',
        'license',
        'requires-python',
        'dependencies'
    ]

    missing_fields = []
    for field in required_fields:
        if f'{field} =' not in content and f'{field}=' not in content:
            missing_fields.append(field)

    if missing_fields:
        print(f"   ❌ Missing metadata fields: {missing_fields}")
        return False

    print("   ✅ Package metadata is complete")
    return True

def check_readme():
    """Check that README contains essential information."""
    print("\n🔍 Checking README...")

    readme_path = Path('README.md')
    if not readme_path.exists():
        print("   ❌ README.md not found")
        return False

    with open(readme_path, 'r') as f:
        content = f.read().lower()

    required_sections = [
        'installation',
        'usage',
        'example'
    ]

    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)

    if missing_sections:
        print(f"   ❌ README missing sections: {missing_sections}")
        return False

    print("   ✅ README contains essential information")
    return True

def check_dependencies():
    """Check that dependencies are reasonable."""
    print("\n🔍 Checking dependencies...")

    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.exists():
        print("   ❌ pyproject.toml not found")
        return False

    with open(pyproject_path, 'r') as f:
        content = f.read()

    # Check that core dependencies are minimal
    core_deps_match = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if core_deps_match:
        core_deps = core_deps_match.group(1)
        if 'openai' in core_deps.lower():
            print("   ⚠️  OpenAI is in core dependencies - consider moving to optional dependencies")
            return False

    print("   ✅ Dependencies look reasonable")
    return True

def main():
    """Main checklist function."""
    print("=" * 60)
    print("📋 PRE-PUBLISHING CHECKLIST - LLM Regression Tester")
    print("=" * 60)

    checks = [
        ("Version Consistency", check_version_consistency),
        ("Required Files", check_required_files),
        ("Package Metadata", check_package_metadata),
        ("README Content", check_readme),
        ("Dependencies", check_dependencies),
    ]

    all_passed = True
    results = []

    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
            if not result:
                all_passed = False
        except Exception as e:
            print(f"   ❌ Error in {check_name}: {e}")
            results.append((check_name, False))
            all_passed = False

    # Summary
    print("\n" + "=" * 60)
    print("📊 CHECKLIST SUMMARY")
    print("=" * 60)

    for check_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{check_name}: {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Ready for publishing.")
        print("\n🚀 Publishing steps:")
        print("1. Update version number if needed")
        print("2. Run: python -m build")
        print("3. Run: twine check dist/*")
        print("4. Run: twine upload dist/*")
        print("5. Create git tag: git tag v{version}")
        print("6. Push tag: git push origin v{version}")
        return 0
    else:
        print("❌ SOME CHECKS FAILED! Please fix issues before publishing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
