import boto3
import json

# Initialize AWS clients at the module level
s3 = boto3.client('s3')
textract = boto3.client('textract')

def lambda_handler(event, context):
    # Parse input event for bucket and object key
    bucket = event.get('bucket', '')
    key = event.get('key', '')

    if not bucket or not key:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Bucket or key not provided."})
        }

    # Download file from S3
    try:
        document = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error fetching file from S3: {e}"})
        }

    # Analyze document with Textract
    try:
        response = textract.analyze_document(
            Document={'Bytes': document},
            FeatureTypes=["TABLES", "FORMS"]
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Textract analysis failed: {e}"})
        }

    # Extract metadata and structure
    structured_data = {
        "text_blocks": response.get("Blocks", []),
        "metadata": {
            "bucket": bucket,
            "key": key
        }
    }

    # Return processed data
    return {
        "statusCode": 200,
        "body": json.dumps(structured_data)
    }
