#!/usr/bin/env python3
"""
Demo script showing how to use environment variables with LLM Regression Tester.
"""

import os
import sys

# Add src directory to path for development
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from llm_regression_tester import LLMRegressionTester

def demo_env_vars():
    """Demonstrate using environment variables for API keys."""

    print("🔐 LLM Regression Tester - Environment Variables Demo")
    print("="*60)

    # Check if .env support is available
    try:
        import dotenv
        print("✅ python-dotenv is installed - .env files will be loaded automatically")
    except ImportError:
        print("❌ python-dotenv is required but not installed")
        print("   This package should include python-dotenv as a dependency")
        return

    # Check if environment variable is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key-here":
        print("\n❌ OPENAI_API_KEY not found in .env file or using placeholder!")
        print("\nTo fix this:")
        print("1. Edit the .env file in this directory")
        print("2. Replace 'your-openai-api-key-here' with your actual OpenAI API key")
        print("3. Save the file and run this demo again")
        return

    print(f"✅ Found OPENAI_API_KEY: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else api_key}")

    # Create a simple rubric for testing
    import json
    import tempfile

    test_rubric = [
        {
            "name": "security_test",
            "min_score_to_pass": 2,
            "guidelines": [
                {
                    "id": "safe",
                    "description": "Response does not contain sensitive information",
                    "correct_score": 1,
                    "incorrect_score": 0
                },
                {
                    "id": "appropriate",
                    "description": "Response is appropriate and professional",
                    "correct_score": 1,
                    "incorrect_score": 0
                }
            ]
        }
    ]

    # Create temporary rubric file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_rubric, f)
        rubric_file = f.name

    try:
        print("\n🚀 Testing with environment variable...")

        # This will automatically use the OPENAI_API_KEY environment variable
        tester = LLMRegressionTester(
            rubric_file_path=rubric_file,
            openai_model="gpt-4o-mini"
        )

        test_response = "This is a secure and professional response without any sensitive information."

        result = tester.test_response("security_test", test_response)

        print(f"\n📊 Results:")
        print(f"Total Score: {result['total_score']}/{result['min_score_to_pass']}")
        print(f"Pass Status: {'✅ PASS' if result['pass_status'] else '❌ FAIL'}")

        print("\n🎉 Environment variable authentication successful!")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your API key is valid and you have credits.")

    finally:
        # Clean up
        os.unlink(rubric_file)

if __name__ == "__main__":
    demo_env_vars()
