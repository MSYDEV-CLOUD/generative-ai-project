import unittest
from unittest.mock import patch
import boto3
import json

class TestWorkflow(unittest.TestCase):
    @patch('boto3.client')
    def test_workflow_execution(self, mock_boto3_client):
        mock_stepfunctions = mock_boto3_client.return_value
        mock_stepfunctions.start_execution.return_value = {
            "executionArn": "arn:aws:states:us-east-1:123456789012:execution:GenerativeAIWorkflow:test-execution"
        }

        stepfunctions = boto3.client('stepfunctions')
        input_data = {
            "bucket": "test-bucket",
            "key": "test-document.pdf",
            "query": "What is this document about?"
        }

        response = stepfunctions.start_execution(
            stateMachineArn="arn:aws:states:us-east-1:123456789012:stateMachine:GenerativeAIWorkflow",
            input=json.dumps(input_data)
        )
        self.assertIn("executionArn", response)

if __name__ == "__main__":
    unittest.main()
