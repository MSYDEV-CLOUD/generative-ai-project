import boto3

def get_logs(log_group_name):
    """Fetches logs from CloudWatch with pagination."""
    logs = boto3.client('logs')
    try:
        paginator = logs.get_paginator('describe_log_streams')
        for page in paginator.paginate(logGroupName=log_group_name, orderBy='LastEventTime', descending=True):
            for log_stream in page.get('logStreams', []):
                print(f"Log Stream: {log_stream['logStreamName']}")
    except Exception as e:
        print(f"Failed to fetch logs: {e}")

if __name__ == "__main__":
    log_group_name = "/aws/lambda/PreprocessingLambda"  # Replace with your Lambda log group name
    get_logs(log_group_name)
