#!/usr/bin/env python3
"""
Easy Assert Examples for LLM Regression Tester

This file demonstrates how to use the simple assert methods for testing LLM responses
against predefined rubrics. These examples show the clean, readable syntax for
writing pass/fail tests.
"""

import os
import sys

# Add src directory to path for development
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from llm_regression_tester import LLMRegressionTester


def test_customer_service_responses():
    """Example: Test customer service response quality."""
    print("🧪 Testing Customer Service Response Quality")
    print("=" * 50)

    # This would normally be your actual tester with API key
    # tester = LLMRegressionTester('path/to/your/rubric.json')

    # For this example, we'll show the syntax (commented out to avoid API calls)

    # GOOD RESPONSE EXAMPLE
    good_response = """
    Hello! Thank you for reaching out to our customer support team.
    I'm happy to help you resolve your billing question. According to our records,
    your last payment of $29.99 was processed successfully on March 15th.
    If you have any other questions, please don't hesitate to contact us again.
    """

    # This would pass the customer service rubric
    # tester.assert_pass("customer_support", good_response,
    #                   "Professional response should pass all quality guidelines")

    # BAD RESPONSE EXAMPLE
    bad_response = "Your bill is paid. Bye."

    # This would fail the customer service rubric
    # tester.assert_fail("customer_support", bad_response,
    #                   "Rude, unhelpful response should fail quality guidelines")

    print("✅ Good response format demonstrated")
    print("❌ Bad response format demonstrated")
    print()


def test_code_quality_reviews():
    """Example: Test code review quality."""
    print("🧪 Testing Code Review Quality")
    print("=" * 50)

    # GOOD CODE REVIEW EXAMPLE
    good_review = """
    The code implements the required functionality correctly. The function is well-documented
    with clear docstrings, follows PEP 8 style guidelines, and includes appropriate error handling.
    The variable names are descriptive and the logic is easy to follow. Overall, this is high-quality code.
    """

    # This would pass the code review rubric
    # tester.assert_pass("code_review", good_review,
    #                   "Comprehensive code review should pass all quality guidelines")

    # BAD CODE REVIEW EXAMPLE
    bad_review = "Looks fine."

    # This would fail the code review rubric
    # tester.assert_fail("code_review", bad_review,
    #                   "Superficial code review should fail quality guidelines")

    print("✅ Good code review format demonstrated")
    print("❌ Bad code review format demonstrated")
    print()


def test_content_moderation():
    """Example: Test content moderation."""
    print("🧪 Testing Content Moderation")
    print("=" * 50)

    # APPROPRIATE CONTENT EXAMPLE
    appropriate_content = """
    This article discusses various programming languages and their use cases
    in modern software development. It covers topics like Python for data science,
    JavaScript for web development, and Go for backend services.
    """

    # This would pass the content moderation rubric
    # tester.assert_pass("content_moderation", appropriate_content,
    #                   "Appropriate technical content should pass moderation")

    # INAPPROPRIATE CONTENT EXAMPLE
    inappropriate_content = "Check out this malicious script that can hack any website instantly!!!"

    # This would fail the content moderation rubric
    # tester.assert_fail("content_moderation", inappropriate_content,
    #                   "Malicious content should fail moderation")

    print("✅ Appropriate content format demonstrated")
    print("❌ Inappropriate content format demonstrated")
    print()


def test_specific_score_requirements():
    """Example: Test for specific score requirements."""
    print("🧪 Testing Specific Score Requirements")
    print("=" * 50)

    response = "This response meets some but not all quality guidelines."

    # Test for exact score
    # tester.assert_score("customer_support", response, 2,
    #                    "Response should score exactly 2 points")

    # Test that it passes (score >= minimum)
    # tester.assert_pass("customer_support", response)

    # Test that it fails (score < minimum)
    # tester.assert_fail("customer_support", response)

    print("📊 Score assertion examples demonstrated")
    print()


def main():
    """Run all example demonstrations."""
    print("🚀 LLM Regression Tester - Easy Assert Method Examples")
    print("=" * 60)
    print()

    print("These examples show how to use the simple assert methods:")
    print("• assert_pass(rubric_name, response, message)")
    print("• assert_fail(rubric_name, response, message)")
    print("• assert_score(rubric_name, response, expected_score, message)")
    print()

    test_customer_service_responses()
    test_code_quality_reviews()
    test_content_moderation()
    test_specific_score_requirements()

    print("📚 How to use in your own tests:")
    print()
    print("# 1. Set up your tester")
    print("tester = LLMRegressionTester('path/to/rubric.json')")
    print()
    print("# 2. Write simple assertions")
    print("tester.assert_pass('customer_support', good_response)")
    print("tester.assert_fail('customer_support', bad_response)")
    print("tester.assert_score('customer_support', response, 3)")
    print()
    print("# 3. Custom error messages")
    print("tester.assert_pass('rubric', response, 'Should pass quality check')")
    print()
    print("✨ That's it! Clean, readable, and powerful LLM testing!")


if __name__ == "__main__":
    main()
