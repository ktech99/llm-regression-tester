# LLM Regression Tester

[![PyPI version](https://badge.fury.io/py/llm-regression-tester.svg)](https://pypi.org/project/llm-regression-tester/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

A Python library for testing LLM responses against predefined rubrics using OpenAI's API for automated scoring. Features easy assert methods for clean, readable tests. Simple, focused, and powerful.

## 🚀 Features

- **OpenAI Integration**: Seamless integration with OpenAI's API
- **Flexible Rubric System**: Define custom evaluation criteria and scoring rules
- **Automated Scoring**: AI-powered evaluation of responses against guidelines
- **Easy Assert Methods**: Simple `assert_pass()`, `assert_fail()`, and `assert_score()` methods for testing
- **Environment Variables**: Support for .env files and environment variables
- **Simple API**: Easy to use with minimal configuration
- **Type Hints**: Full type annotation support for better IDE experience
- **Comprehensive Testing**: Built-in test examples and utilities

## 📦 Installation

### Basic Installation
```bash
pip install llm-regression-tester
```

### Environment Variables
The library uses .env files to securely store your API keys:

#### .env File Setup (Required)
```bash
# Create a .env file in your project root
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env

# Edit the .env file with your actual API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Important:** The library automatically loads `.env` files. Make sure `.env` is in your `.gitignore` to keep your keys secure.

## 🔧 Quick Start

### 1. Create a Rubric File

Create a JSON file defining your evaluation criteria:

```json
[
  {
    "name": "customer_support_response",
    "min_score_to_pass": 7,
    "guidelines": [
      {
        "id": "polite",
        "description": "Response is polite and professional",
        "correct_score": 3,
        "incorrect_score": 0
      },
      {
        "id": "accurate",
        "description": "Response provides accurate information",
        "correct_score": 2,
        "incorrect_score": 0
      },
      {
        "id": "helpful",
        "description": "Response offers specific help or next steps",
        "correct_score": 2,
        "incorrect_score": 0
      }
    ]
  }
]
```

### 2. Basic Usage

```python
from llm_regression_tester import LLMRegressionTester

# Option 1: Initialize with API key parameter
tester = LLMRegressionTester(
    rubric_file_path="rubrics.json",
    openai_api_key="your-openai-api-key"
)

# Option 2: Initialize with .env file (recommended for security)
# Create a .env file with: OPENAI_API_KEY=your-actual-api-key
tester = LLMRegressionTester(
    rubric_file_path="rubrics.json"
    # API key will be automatically loaded from .env file
)

# Test a response
result = tester.test_response("customer_support_response", "Thank you for your question...")
print(f"Score: {result['total_score']}/{result['min_score_to_pass']}")
print(f"Pass: {result['pass_status']}")

# Or use easy assert methods for testing
tester.assert_pass("customer_support_response", "Thank you for your question...")
tester.assert_fail("customer_support_response", "This is a terrible response.")
tester.assert_score("customer_support_response", "Good response", 7)
```

### 3. Easy Assert Methods for Testing

The library provides simple assert methods that make testing LLM responses intuitive and readable:

```python
from llm_regression_tester import LLMRegressionTester

tester = LLMRegressionTester("rubrics.json")

# Assert that a response passes the rubric
tester.assert_pass("customer_support", good_response)

# Assert that a response fails the rubric
tester.assert_fail("customer_support", bad_response)

# Assert a specific score
tester.assert_score("customer_support", response, 8)

# Custom error messages
tester.assert_pass("rubric", response, "Professional response should pass quality check")
```

**Benefits:**
- **Clean Syntax**: One-line assertions instead of multiple lines of result checking
- **Clear Errors**: Helpful error messages showing exactly what failed and why
- **Flexible**: Optional custom messages for better test documentation
- **Powerful**: Supports pass/fail/score assertions for comprehensive testing

### 4. Using .env Files

```python
from llm_regression_tester import LLMRegressionTester

# Create a .env file with your API key:
# OPENAI_API_KEY=your-actual-api-key

# Initialize without API key parameter
tester = LLMRegressionTester("rubrics.json")
# API key will be automatically loaded from .env file

result = tester.test_response("customer_support_response", "Hello, how can I help?")
print(f"Score: {result['total_score']}/{result['min_score_to_pass']}")
```

### 5. Test Examples

The library includes comprehensive test examples showing how to use the assert methods in practice:

```bash
# Run the test examples
python test_examples.py
```

This demonstrates:
- Customer service response quality testing
- Code review evaluation
- Content moderation
- Practical usage patterns with the assert methods

### Running Tests

```bash
# Run all tests
pytest

# Run specific test examples
pytest tests/test_basic.py::test_assert_pass_method -v

# Run the example demonstration
python test_examples.py
```

## 📋 API Reference

### LLMRegressionTester

#### Constructor
```python
LLMRegressionTester(
    rubric_file_path: str,
    openai_api_key: Optional[str] = None,
    openai_model: str = "gpt-4o-mini"
)
```

**Parameters:**
- `rubric_file_path`: Path to JSON file containing rubrics
- `openai_api_key`: OpenAI API key. If None, will check OPENAI_API_KEY environment variable
- `openai_model`: OpenAI model to use (default: gpt-4o-mini)

#### Methods

##### `test_response(name: str, response: str) -> Dict[str, Any]`
Test a response against a specific rubric.

**Returns:**
```python
{
    "total_score": int,
    "pass_status": bool,
    "min_score_to_pass": int,
    "details": [
        {
            "id": str,
            "description": str,
            "meets": bool,
            "score": int
        }
    ]
}
```

##### `get_available_rubrics() -> List[str]`
Get list of available rubric names.

##### `get_rubric_details(name: str) -> Optional[Dict[str, Any]]`
Get details of a specific rubric.

##### `assert_pass(rubric_name: str, response: str, message: str = None) -> None`
Assert that a response passes the specified rubric test. Raises AssertionError if the test fails.

##### `assert_fail(rubric_name: str, response: str, message: str = None) -> None`
Assert that a response fails the specified rubric test. Raises AssertionError if the test passes when it should fail.

##### `assert_score(rubric_name: str, response: str, expected_score: int, message: str = None) -> None`
Assert that a response achieves a specific score. Raises AssertionError if the score doesn't match.

## 🏗️ Architecture

The library has a simple, focused architecture:

```
LLMRegressionTester
├── Rubric Management (JSON file loading and validation)
├── OpenAI Integration (direct API calls)
├── Response Evaluation (automated scoring)
└── Assert Methods (easy testing with assert_pass/fail/score)
```

**Key Components:**
- **Rubric System**: JSON-based evaluation criteria
- **OpenAI Client**: Direct integration with OpenAI's API
- **Assert Methods**: Simple `assert_pass()`, `assert_fail()`, and `assert_score()` methods
- **Environment Support**: Automatic loading from .env files and environment variables
- **Error Handling**: Comprehensive validation and error reporting

## 📝 Rubric Format

Rubrics are defined in JSON format:

```json
{
  "name": "rubric_name",
  "min_score_to_pass": 7,
  "guidelines": [
    {
      "id": "unique_id",
      "description": "Description of the criterion",
      "correct_score": 2,
      "incorrect_score": 0
    }
  ]
}
```

## 🔐 Environment Variables

The library supports the following environment variables for API keys:

- `OPENAI_API_KEY`: OpenAI API key for GPT models

**Security Best Practices:**
- Never commit API keys to version control
- Use environment variables or secure credential management
- Rotate keys regularly
- Use different keys for development and production

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Guidelines

1. Follow the existing code style and patterns
2. Add comprehensive tests for new features
3. Update documentation for any changes
4. Ensure backward compatibility when possible
5. Test with different rubric configurations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern Python packaging standards
- Inspired by the need for standardized LLM evaluation
- Thanks to all contributors and the open-source community

## 📞 Support

- 📧 [Issues](https://github.com/ktech99/llm-regression-tester/issues)
- 📚 [Documentation](https://llm-regression-tester.readthedocs.io/)
- 💬 [Discussions](https://github.com/ktech99/llm-regression-tester/discussions)

---

**Happy Testing!** 🎉
