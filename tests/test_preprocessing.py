import unittest
from unittest.mock import patch, Mock
from src.lambda_functions.preprocessing.preprocess import lambda_handler

class TestPreprocessingLambda(unittest.TestCase):
    @patch('boto3.client')
    def test_lambda_handler_success(self, mock_boto3_client):
        # Separate mock instances for S3 and Textract
        mock_s3 = Mock()
        mock_textract = Mock()
        mock_boto3_client.side_effect = lambda service: mock_s3 if service == "s3" else mock_textract

        # Mock responses
        mock_s3.get_object.return_value = {'Body': b'test-content'}
        mock_textract.analyze_document.return_value = {
            "Blocks": [{"BlockType": "LINE", "Text": "Sample text"}]
        }

        event = {
            "bucket": "test-bucket",
            "key": "test-document.pdf"
        }

        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("text_blocks", response["body"])

    def test_lambda_handler_missing_input(self):
        event = {}
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)

if __name__ == "__main__":
    unittest.main()
