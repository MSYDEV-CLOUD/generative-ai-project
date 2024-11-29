import boto3

def upload_to_s3(bucket_name, key, file_path):
    """Uploads a file to an S3 bucket."""
    s3 = boto3.client('s3')
    try:
        with open(file_path, 'rb') as file_data:
            s3.upload_fileobj(file_data, bucket_name, key)
        print(f"File uploaded successfully to s3://{bucket_name}/{key}")
    except Exception as e:
        print(f"Failed to upload file: {e}")

if __name__ == "__main__":
    # Define the bucket, key, and local file path
    bucket_name = "generative-ai-project-data"
    key = "test-document.pdf"
    file_path = "path/to/your/test-document.pdf"

    upload_to_s3(bucket_name, key, file_path)
