#!/usr/bin/env python3
"""
Simple script to test that llm_regression_tester can be imported successfully.
"""

import sys
import os

# Add src directory to path for development
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from llm_regression_tester import LLMRegressionTester, __version__
    print("✅ Import successful!")
    print(f"📦 Package version: {__version__}")
    print("🎉 Ready to use LLMRegressionTester!")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
