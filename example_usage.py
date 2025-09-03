"""
Example usage of the LLMRegressionTester library.

This example demonstrates how to:
1. Create a rubric JSON file
2. Use OpenAI API for automated testing
3. Test responses against rubrics
"""

import json
import sys
import os
from typing import Dict, Any

# Add src directory to path for development
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from llm_regression_tester import LLMRegressionTester

# Example rubric data
sample_rubric_data = [
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
            },
            {
                "id": "complete",
                "description": "Response addresses all aspects of the query",
                "correct_score": 2,
                "incorrect_score": 0
            },
            {
                "id": "concise",
                "description": "Response is clear and not unnecessarily verbose",
                "correct_score": 1,
                "incorrect_score": 0
            }
        ]
    },
    {
        "name": "code_review",
        "min_score_to_pass": 6,
        "guidelines": [
            {
                "id": "functionality",
                "description": "Code maintains intended functionality",
                "correct_score": 2,
                "incorrect_score": 0
            },
            {
                "id": "readability",
                "description": "Code is readable and well-documented",
                "correct_score": 2,
                "incorrect_score": 0
            },
            {
                "id": "efficiency",
                "description": "Code is efficient and optimized",
                "correct_score": 2,
                "incorrect_score": 0
            },
            {
                "id": "best_practices",
                "description": "Code follows language best practices",
                "correct_score": 2,
                "incorrect_score": 0
            }
        ]
    }
]

def create_sample_rubric_file():
    """Create a sample rubric file for testing."""
    with open('sample_rubric.json', 'w') as f:
        json.dump(sample_rubric_data, f, indent=2)
    print("Created sample_rubric.json")

def demonstrate_openai_direct():
    """Demonstrate usage with OpenAI API key provided directly."""
    print("\n" + "="*50)
    print("DEMONSTRATION: OpenAI with Direct API Key")
    print("="*50)

    try:
        # Get API key from environment variable (supports .env files)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your-openai-api-key-here":
            print("❌ Please set your OpenAI API key in the .env file")
            print("   Edit the .env file and replace 'your-openai-api-key-here' with your actual key")
            return

        tester = LLMRegressionTester(
            rubric_file_path='sample_rubric.json',
            openai_api_key=api_key,
            openai_model="gpt-4o-mini"
        )

        test_response = """
        Thank you for contacting our customer support. I'm happy to help you with your billing question.
        According to our records, your last payment was processed on March 15th for $29.99.
        If you need to update your payment method or have any other questions, please let me know.
        """

        # You can use the detailed result
        result = tester.test_response('customer_support_response', test_response)
        display_results(result)

        # Or use the simple assert methods (recommended for testing)
        # These will raise AssertionError if the test fails
        # tester.assert_pass('customer_support_response', test_response,
        #                   "Customer support response should meet all quality guidelines")

    except Exception as e:
        print(f"❌ OpenAI example requires valid API key: {e}")
        print("💡 Tip: Replace 'your-openai-api-key-here' with your actual OpenAI API key")

def demonstrate_openai_env():
    """Demonstrate usage with OpenAI API key from environment variable."""
    print("\n" + "="*50)
    print("DEMONSTRATION: OpenAI with Environment Variable")
    print("="*50)

    print("🔧 To use this demo, set your OpenAI API key as an environment variable:")
    print("   export OPENAI_API_KEY='your-actual-api-key'")
    print("   # Or add it to a .env file: OPENAI_API_KEY=your-actual-api-key")
    print()

    try:
        # This will automatically use the OPENAI_API_KEY environment variable
        tester = LLMRegressionTester(
            rubric_file_path='sample_rubric.json',
            openai_model="gpt-4o-mini"
        )

        test_response = """
        Thank you for contacting our customer support. I'm happy to help you with your billing question.
        According to our records, your last payment was processed on March 15th for $29.99.
        If you need to update your payment method or have any other questions, please let me know.
        """

        result = tester.test_response('customer_support_response', test_response)
        display_results(result)

    except Exception as e:
        print(f"❌ OpenAI environment variable example failed: {e}")
        print("💡 Make sure OPENAI_API_KEY is set in your environment or .env file")

def demonstrate_code_review():
    """Demonstrate usage with code review rubric."""
    print("\n" + "="*50)
    print("DEMONSTRATION: Code Review Rubric")
    print("="*50)

    try:
        # Get API key from environment variable (supports .env files)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your-openai-api-key-here":
            print("❌ Please set your OpenAI API key in the .env file")
            print("   Edit the .env file and replace 'your-openai-api-key-here' with your actual key")
            return

        tester = LLMRegressionTester(
            rubric_file_path='sample_rubric.json',
            openai_api_key=api_key,
            openai_model="gpt-4o-mini"
        )

        code_sample = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
        """

        result = tester.test_response('code_review', code_sample.strip())
        display_results(result)

    except Exception as e:
        print(f"❌ Code review example failed: {e}")
        print("💡 Replace 'your-openai-api-key-here' with your actual OpenAI API key")

def display_results(result: Dict[str, Any]):
    """Display test results in a formatted way."""
    print(f"\nTotal Score: {result['total_score']}/{result['min_score_to_pass']}")
    print(f"Pass Status: {'✅ PASS' if result['pass_status'] else '❌ FAIL'}")

    print("\nDetailed Breakdown:")
    for detail in result['details']:
        status = "✅" if detail['meets'] else "❌"
        print(f"  {status} {detail['description']}")
        print(f"     Score: {detail['score']}")
        if 'error' in detail:
            print(f"     Error: {detail['error']}")

def main():
    """Main demonstration function."""
    print("LLM Regression Tester - OpenAI Examples")
    print("="*60)

    # Create sample rubric file
    create_sample_rubric_file()

    # Run demonstrations
    print("\n🚀 Running demonstrations...")
    demonstrate_openai_direct()
    demonstrate_openai_env()
    demonstrate_code_review()

    print("\n" + "="*60)
    print("📚 To use these examples:")
    print("1. Edit the .env file and replace 'your-openai-api-key-here' with your actual OpenAI API key")
    print("2. Make sure python-dotenv is installed (it should be installed with this package)")

    # Show available rubrics
    try:
        # Try to load rubrics without initializing OpenAI client
        import json
        with open('sample_rubric.json', 'r') as f:
            rubrics_data = json.load(f)
        rubric_names = [rubric['name'] for rubric in rubrics_data]
        print(f"\n📋 Available rubrics: {rubric_names}")
    except Exception as e:
        print(f"\n📋 Error loading rubrics: {e}")
        print("Make sure sample_rubric.json exists by running the demonstrations above")

if __name__ == "__main__":
    main()
