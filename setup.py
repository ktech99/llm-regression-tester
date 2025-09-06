#!/usr/bin/env python3
"""
Setup script for LLM Regression rubric.
"""

from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-regression-rubric",
    version="0.1.1",
    author="LLM Regression Tester Contributors",
    description="A flexible library for testing LLM responses against predefined rubrics using OpenAI's API for automated scoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ktech99/llm-regression-tester",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typing-extensions>=4.0.0",
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
    ],
    keywords="llm testing evaluation rubrics ai nlp",
    project_urls={
        "Homepage": "https://github.com/ktech99/llm-regression-tester",
        "Documentation": "https://llm-regression-tester.readthedocs.io/",
        "Repository": "https://github.com/ktech99/llm-regression-tester.git",
        "Issues": "https://github.com/ktech99/llm-regression-tester/issues",
        "Changelog": "https://github.com/ktech99/llm-regression-tester/blob/main/CHANGELOG.md",
    },
)
