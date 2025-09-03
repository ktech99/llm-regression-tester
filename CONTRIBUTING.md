# Contributing to LLM Regression Tester

Thank you for your interest in contributing to LLM Regression Tester! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/ktech99/llm-regression-tester.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install development dependencies: `pip install -e ".[all,dev]"`

## Development Setup

```bash
# Install in development mode with all dependencies
pip install -e ".[all,dev]"

# Run tests
pytest

# Run linting
black src/
isort src/
mypy src/
```

## Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking
- **pytest** for testing

Please ensure your code passes all checks before submitting a PR.

## Adding New LLM Providers

To add support for a new LLM provider:

1. Extend the `LLMProvider` abstract base class
2. Implement the `evaluate_response` method
3. Add tests for your provider
4. Update documentation

Example:

```python
from llm_regression_tester import LLMProvider

class MyLLMProvider(LLMProvider):
    def __init__(self, api_key: str):
        # Initialize your provider
        pass

    def evaluate_response(self, prompt: str, **kwargs) -> str:
        # Implement your LLM logic
        return "Yes"  # or "No"
```

## Testing

Add tests for new features in the `tests/` directory. Run tests with:

```bash
pytest tests/
```

## Documentation

- Update README.md for new features
- Add docstrings to all public methods
- Update type hints

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run tests and linting
4. Update documentation if needed
5. Commit your changes: `git commit -m "Add my feature"`
6. Push to your fork: `git push origin feature/my-feature`
7. Create a Pull Request

## Issues

- Check existing issues before creating new ones
- Use clear, descriptive titles
- Provide steps to reproduce bugs
- Include error messages and stack traces

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to create a welcoming environment for all contributors.

## License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.
