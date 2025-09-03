#!/usr/bin/env python3
"""
Runner script for LLM Regression Tester examples.

This script sets up the proper Python path and runs the examples.
"""

import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import and run the examples
from example_usage import main

if __name__ == "__main__":
    main()
