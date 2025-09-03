"""
LLM Regression Tester

A flexible library for testing LLM responses against predefined rubrics using OpenAI's API for automated scoring.
"""

import json
import logging
import os
from typing import Dict, List, Any, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMRegressionTester:
    """
    A class for testing LLM responses against predefined rubrics using OpenAI's API.

    This class loads rubrics from a JSON file and uses OpenAI's API to evaluate
    whether responses meet specified guidelines.
    """

    def __init__(
        self,
        rubric_file_path: str,
        openai_api_key: Optional[str] = None,
        openai_model: str = "gpt-4o-mini"
    ):
        """
        Initialize the tester with the path to the JSON rubric file and OpenAI credentials.

        Args:
            rubric_file_path: Path to the JSON file containing rubrics
            openai_api_key: OpenAI API key. If None, will load from .env file
            openai_model: OpenAI model to use (default: gpt-4o-mini)

        Examples:
            # Using API key parameter
            tester = LLMRegressionTester("rubrics.json", openai_api_key="your-key")

            # Using .env file (recommended)
            tester = LLMRegressionTester("rubrics.json")  # Will load OPENAI_API_KEY from .env file
        """
        try:
            # Get API key from parameter or environment variable
            self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key is required. Provide it as a parameter "
                    "or add OPENAI_API_KEY to your .env file."
                )

            # Initialize OpenAI client
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                self.model = openai_model
            except ImportError:
                raise ImportError("openai package is required. Install with: pip install openai")

            # Load rubrics
            self.rubrics = self._load_rubrics(rubric_file_path)

        except Exception as e:
            logger.error(f"Failed to initialize LLMRegressionTester: {e}")
            raise

    def _load_rubrics(self, file_path: str) -> Dict[str, Any]:
        """
        Load rubrics from a JSON file.

        Args:
            file_path: Path to the JSON file containing rubrics

        Returns:
            Dictionary mapping rubric names to rubric objects

        Raises:
            FileNotFoundError: If the rubric file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
            ValueError: If the rubric structure is invalid
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("Rubric file must contain a list of rubric objects")

            rubrics_dict = {}
            for rubric in data:
                self._validate_rubric_structure(rubric)
                rubrics_dict[rubric['name']] = rubric

            logger.info(f"Successfully loaded {len(rubrics_dict)} rubrics from {file_path}")
            return rubrics_dict

        except FileNotFoundError:
            raise FileNotFoundError(f"Rubric file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in rubric file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading rubrics: {e}")

    def _validate_rubric_structure(self, rubric: Dict[str, Any]) -> None:
        """
        Validate that a rubric has the required structure.

        Args:
            rubric: Rubric dictionary to validate

        Raises:
            ValueError: If the rubric structure is invalid
        """
        required_keys = ['name', 'guidelines', 'min_score_to_pass']
        for key in required_keys:
            if key not in rubric:
                raise ValueError(f"Rubric missing required key: {key}")

        if not isinstance(rubric['guidelines'], list):
            raise ValueError("Rubric 'guidelines' must be a list")

        for guideline in rubric['guidelines']:
            required_guideline_keys = ['id', 'description', 'correct_score', 'incorrect_score']
            for key in required_guideline_keys:
                if key not in guideline:
                    raise ValueError(f"Guideline missing required key: {key}")

    def test_response(self, name: str, response: str) -> Dict[str, Any]:
        """
        Test the given response against the rubric specified by name.

        Args:
            name: Name of the rubric to test against
            response: The response text to evaluate

        Returns:
            Dictionary with total_score, pass_status, min_score_to_pass, and details

        Raises:
            ValueError: If the rubric name is not found or inputs are invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Rubric name must be a non-empty string")

        if not response or not isinstance(response, str):
            raise ValueError("Response must be a non-empty string")

        if name not in self.rubrics:
            available_rubrics = list(self.rubrics.keys())
            raise ValueError(f"Rubric '{name}' not found. Available rubrics: {available_rubrics}")

        rubric = self.rubrics[name]
        guidelines = rubric['guidelines']
        min_score = rubric['min_score_to_pass']

        total_score = 0
        details = []

        for guideline in guidelines:
            try:
                meets = self._evaluate_guideline(guideline, response)
                score = guideline['correct_score'] if meets else guideline['incorrect_score']
                total_score += score

                details.append({
                    "id": guideline['id'],
                    "description": guideline['description'],
                    "meets": meets,
                    "score": score
                })
            except Exception as e:
                logger.error(f"Error evaluating guideline {guideline['id']}: {e}")
                # Continue with other guidelines, mark this one as failed
                details.append({
                    "id": guideline['id'],
                    "description": guideline['description'],
                    "meets": False,
                    "score": guideline['incorrect_score'],
                    "error": str(e)
                })

        pass_status = total_score >= min_score

        result = {
            "total_score": total_score,
            "pass_status": pass_status,
            "min_score_to_pass": min_score,
            "details": details
        }

        logger.info(f"Test completed for rubric '{name}': Score {total_score}/{min_score}, Pass: {pass_status}")
        return result

    def assert_pass(self, rubric_name: str, response: str, message: str = None) -> None:
        """
        Assert that a response passes the specified rubric test.

        Args:
            rubric_name: Name of the rubric to test against
            response: The response text to evaluate
            message: Optional custom message for assertion failure

        Raises:
            AssertionError: If the response does not pass the rubric test
        """
        result = self.test_response(rubric_name, response)

        if not result["pass_status"]:
            default_message = (
                f"Response failed rubric '{rubric_name}': "
                f"Score {result['total_score']}/{result['min_score_to_pass']}\n"
                f"Failed guidelines: {[d['description'] for d in result['details'] if not d['meets']]}"
            )
            raise AssertionError(message or default_message)

    def assert_fail(self, rubric_name: str, response: str, message: str = None) -> None:
        """
        Assert that a response fails the specified rubric test.

        Args:
            rubric_name: Name of the rubric to test against
            response: The response text to evaluate
            message: Optional custom message for assertion failure

        Raises:
            AssertionError: If the response passes the rubric test (when it should fail)
        """
        result = self.test_response(rubric_name, response)

        if result["pass_status"]:
            default_message = (
                f"Response unexpectedly passed rubric '{rubric_name}': "
                f"Score {result['total_score']}/{result['min_score_to_pass']}\n"
                f"This test expected the response to fail the rubric."
            )
            raise AssertionError(message or default_message)

    def assert_score(self, rubric_name: str, response: str, expected_score: int, message: str = None) -> None:
        """
        Assert that a response achieves a specific score for the rubric.

        Args:
            rubric_name: Name of the rubric to test against
            response: The response text to evaluate
            expected_score: The expected total score
            message: Optional custom message for assertion failure

        Raises:
            AssertionError: If the response score doesn't match the expected score
        """
        result = self.test_response(rubric_name, response)

        if result["total_score"] != expected_score:
            default_message = (
                f"Response score mismatch for rubric '{rubric_name}': "
                f"Expected {expected_score}, got {result['total_score']}\n"
                f"Pass status: {result['pass_status']}"
            )
            raise AssertionError(message or default_message)

    def _evaluate_guideline(self, guideline: Dict[str, Any], response: str) -> bool:
        """
        Evaluate if a response meets a specific guideline using OpenAI.

        Args:
            guideline: Guideline dictionary containing description and scores
            response: Response text to evaluate

        Returns:
            True if the response meets the guideline, False otherwise
        """
        eval_prompt = f"""
        Evaluate the following response against this guideline: "{guideline['description']}"
        Response: "{response}"

        Does the response meet the guideline? Respond with only 'Yes' or 'No'.
        """

        try:
            response_obj = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": eval_prompt}],
                max_tokens=10,  # Small token limit to ensure concise response
                temperature=0   # Deterministic responses
            )

            llm_answer = response_obj.choices[0].message.content.strip().lower()

            # More robust parsing of LLM response
            if llm_answer.startswith('yes'):
                return True
            elif llm_answer.startswith('no'):
                return False
            else:
                logger.warning(f"Unexpected LLM response: '{llm_answer}'. Treating as 'No'.")
                return False

        except Exception as e:
            logger.error(f"Error during LLM evaluation: {e}")
            raise

    def get_available_rubrics(self) -> List[str]:
        """
        Get a list of available rubric names.

        Returns:
            List of rubric names
        """
        return list(self.rubrics.keys())

    def get_rubric_details(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get details of a specific rubric.

        Args:
            name: Name of the rubric

        Returns:
            Rubric dictionary or None if not found
        """
        return self.rubrics.get(name)
