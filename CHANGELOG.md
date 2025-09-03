# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-XX

### Added
- Initial release of LLM Regression Tester
- OpenAI integration for automated LLM response evaluation
- Flexible rubric system for defining evaluation criteria
- Easy assert methods: `assert_pass()`, `assert_fail()`, `assert_score()`
- Environment variable support via `.env` files
- Comprehensive test suite with examples
- Full type annotations and documentation
- CI/CD workflow with GitHub Actions

### Features
- **Automated Scoring**: AI-powered evaluation of responses against predefined guidelines
- **Custom Rubrics**: JSON-based evaluation criteria with configurable scoring rules
- **Simple API**: Easy-to-use methods for testing LLM responses
- **Environment Security**: Secure API key management via `.env` files
- **Assertion Methods**: Clean, readable test assertions for pass/fail/score validation
- **Comprehensive Testing**: Built-in examples and test utilities
- **Type Safety**: Full type annotations for better IDE support and error prevention

### Dependencies
- `openai>=1.0.0`: OpenAI API integration
- `python-dotenv>=0.19.0`: Environment variable loading
- `typing-extensions>=4.0.0`: Enhanced type annotations

### Documentation
- Complete README with usage examples
- API reference documentation
- Test examples and demonstrations
- Installation and setup instructions

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities
