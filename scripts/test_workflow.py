import boto3
import json

def trigger_step_function(state_machine_arn, input_data):
    """Triggers the Step Functions workflow."""
    stepfunctions = boto3.client('stepfunctions')
    try:
        response = stepfunctions.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_data)
        )
        print(f"Step Functions workflow triggered successfully. Execution ARN: {response['executionArn']}")
    except Exception as e:
        print(f"Failed to trigger workflow: {e}")

if __name__ == "__main__":
    # Define the Step Functions ARN and input data
    state_machine_arn = "arn:aws:states:<REGION>:<ACCOUNT_ID>:stateMachine:GenerativeAIWorkflow"
    input_data = {
        "bucket": "generative-ai-project-data",
        "key": "test-document.pdf",
        "query": "What is this document about?"
    }

    trigger_step_function(state_machine_arn, input_data)
