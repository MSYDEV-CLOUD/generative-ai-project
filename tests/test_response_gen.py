import unittest
from unittest.mock import patch
from src.lambda_functions.response_generation.generate_response import lambda_handler

class TestResponseGenerationLambda(unittest.TestCase):
    @patch('openai.OpenAI.generate_response')
    def test_lambda_handler_success(self, mock_generate_response):
        # Mock LLM response
        mock_generate_response.return_value = "Mock response."

        event = {
            "query": "What is this document about?"
        }

        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("response", response["body"])

    def test_lambda_handler_missing_input(self):
        event = {}
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)

if __name__ == "__main__":
    unittest.main()
