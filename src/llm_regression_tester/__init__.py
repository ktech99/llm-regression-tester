"""
LLM Regression Tester

A flexible library for testing LLM responses against predefined rubrics using automated scoring.
Supports multiple LLM providers through a simple interface.
"""

from .llm_regression_tester import LLMRegressionTester
from ._version import __version__, __version_info__

__all__ = [
    "LLMRegressionTester",
    "__version__",
    "__version_info__"
]
