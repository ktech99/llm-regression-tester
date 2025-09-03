"""
Basic tests for LLM Regression Tester.
"""

import json
import tempfile
import os
import sys
import pytest

# Add src directory to path for development
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from llm_regression_tester import LLMRegressionTester


# Sample rubric data for testing
TEST_RUBRIC = [
    {
        "name": "test_rubric",
        "min_score_to_pass": 3,
        "guidelines": [
            {
                "id": "test1",
                "description": "Test guideline 1",
                "correct_score": 2,
                "incorrect_score": 0
            },
            {
                "id": "test2",
                "description": "Test guideline 2",
                "correct_score": 1,
                "incorrect_score": 0
            }
        ]
    }
]


class MockProvider:
    """Mock LLM provider for testing."""

    def __init__(self, response: str = "Yes"):
        self.response = response

    def evaluate_response(self, prompt: str, **kwargs) -> str:
        return self.response


@pytest.fixture
def sample_rubric_file():
    """Create a temporary rubric file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(TEST_RUBRIC, f)
        return f.name


def test_openai_with_api_key_parameter(sample_rubric_file):
    """Test LLMRegressionTester with API key provided as parameter."""
    # Mock the OpenAI client to avoid actual API calls
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Yes"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-api-key"
        )

        result = tester.test_response("test_rubric", "Test response")
        assert result["total_score"] == 3  # 2 + 1
        assert result["pass_status"] is True
        assert len(result["details"]) == 2


def test_openai_provider_failure(sample_rubric_file):
    """Test OpenAI provider returning 'No'."""
    # Mock the OpenAI client to return "No"
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "No"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-key"
        )

        result = tester.test_response("test_rubric", "Test response")
        assert result["total_score"] == 0  # Both guidelines fail
        assert result["pass_status"] is False


def test_available_rubrics(sample_rubric_file):
    """Test getting available rubrics."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-key"
        )

        rubrics = tester.get_available_rubrics()
        assert "test_rubric" in rubrics


def test_get_rubric_details(sample_rubric_file):
    """Test getting rubric details."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-key"
        )

        details = tester.get_rubric_details("test_rubric")
        assert details is not None
        assert details["name"] == "test_rubric"
        assert len(details["guidelines"]) == 2


def test_invalid_rubric_name(sample_rubric_file):
    """Test error handling for invalid rubric name."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-key"
        )

        with pytest.raises(ValueError, match="Rubric 'nonexistent' not found"):
            tester.test_response("nonexistent", "Test response")


def test_invalid_inputs(sample_rubric_file):
    """Test error handling for invalid inputs."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-key"
        )

        with pytest.raises(ValueError, match="Rubric name must be a non-empty string"):
            tester.test_response("", "Test response")

        with pytest.raises(ValueError, match="Response must be a non-empty string"):
            tester.test_response("test_rubric", "")


def test_openai_missing_api_key(sample_rubric_file):
    """Test LLMRegressionTester raises error when no API key is available."""
    # Remove environment variable if it exists
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    with pytest.raises(ValueError, match="OpenAI API key is required"):
        LLMRegressionTester(rubric_file_path=sample_rubric_file)


def test_llm_regression_tester_with_env_var(monkeypatch, sample_rubric_file):
    """Test LLMRegressionTester with environment variable for API key."""
    # Mock environment variable
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

    # Mock the OpenAI client to avoid actual API calls
    import sys
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Yes"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    with patch('openai.OpenAI', return_value=mock_client):
        # This should work without providing openai_api_key parameter
        tester = LLMRegressionTester(rubric_file_path=sample_rubric_file)

        # Verify the client was initialized
        assert tester.client == mock_client
        assert tester.api_key == "test-api-key"


# ============================================================================
# EASY ASSERT METHOD TESTS - Examples for users
# ============================================================================

def test_assert_pass_method(sample_rubric_file):
    """Test the assert_pass method with a passing response."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Yes"  # Mock LLM saying the guideline is met
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-api-key"
        )

        # This should pass without raising an exception
        good_response = "This is a well-written, professional response that meets all guidelines."
        tester.assert_pass("test_rubric", good_response)


def test_assert_fail_method(sample_rubric_file):
    """Test the assert_fail method with a failing response."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "No"  # Mock LLM saying the guideline is NOT met
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-api-key"
        )

        # This should pass without raising an exception (asserting that it fails)
        bad_response = "This is a terrible response that doesn't meet any guidelines."
        tester.assert_fail("test_rubric", bad_response)


def test_assert_score_method(sample_rubric_file):
    """Test the assert_score method."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Yes"  # First guideline met
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-api-key"
        )

        # Should score 3 (2 + 1 from TEST_RUBRIC)
        response = "This response meets the first guideline but not the second."
        tester.assert_score("test_rubric", response, 3)


def test_assert_pass_with_custom_message(sample_rubric_file):
    """Test assert_pass with custom error message."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "No"  # Mock LLM saying guideline is NOT met
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-api-key"
        )

        # This should fail with custom message
        bad_response = "This response is terrible."
        try:
            tester.assert_pass("test_rubric", bad_response, "Custom error: Response quality is poor")
            assert False, "Should have raised AssertionError"
        except AssertionError as e:
            assert "Custom error: Response quality is poor" in str(e)


# ============================================================================
# PRACTICAL EXAMPLES - How users would write tests
# ============================================================================

def test_customer_support_response_quality(sample_rubric_file):
    """Example: Test customer support response quality."""
    from unittest.mock import MagicMock, patch

    # Mock responses for different guidelines
    def mock_response_for_guideline(guideline_id):
        responses = {
            "test1": "Yes",  # Polite and professional
            "test2": "Yes"   # Provides accurate information
        }
        return responses.get(guideline_id, "No")

    mock_client = MagicMock()

    def mock_create(**kwargs):
        prompt = kwargs.get('messages', [{}])[0].get('content', '')
        # Determine which guideline is being tested based on prompt
        if "test1" in prompt:
            response_text = "Yes"
        elif "test2" in prompt:
            response_text = "Yes"
        else:
            response_text = "No"

        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = response_text
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        return mock_response

    mock_client.chat.completions.create.side_effect = mock_create

    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-api-key"
        )

        # Test a good customer support response
        good_response = """
        Thank you for contacting our customer support team. I'm happy to help you with your billing inquiry.
        According to our records, your last payment was processed successfully on March 15th.
        If you need any additional assistance, please don't hesitate to ask.
        """

        # This should pass our rubric
        tester.assert_pass("test_rubric", good_response.strip(),
                         "Good customer support response should pass all quality guidelines")


def test_code_review_quality(sample_rubric_file):
    """Example: Test code review quality (using same rubric for demo)."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "No"  # Mock poor code review
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    with patch('openai.OpenAI', return_value=mock_client):
        tester = LLMRegressionTester(
            rubric_file_path=sample_rubric_file,
            openai_api_key="test-api-key"
        )

        # Test a poor code review
        poor_review = "Code looks ok"

        # This should fail our rubric (and we assert that it fails)
        tester.assert_fail("test_rubric", poor_review,
                          "Poor code review should fail quality guidelines")
