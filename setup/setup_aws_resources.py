import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# File path for .env
env_file_path = os.path.join(os.getcwd(), ".env")

# Initialize AWS clients using region from .env
region = os.getenv("AWS_REGION", "us-east-1")
s3 = boto3.client('s3', region_name=region)
dynamodb = boto3.client('dynamodb', region_name=region)
iam = boto3.client('iam', region_name=region)
opensearch = boto3.client('opensearch', region_name=region)
rds = boto3.client('rds', region_name=region)


def update_env_file(key, value):
    """Update or append key-value pairs in the .env file."""
    with open(env_file_path, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        updated = False
        for line in lines:
            if line.startswith(key + "="):
                file.write(f"{key}={value}\n")
                updated = True
            else:
                file.write(line)
        if not updated:
            file.write(f"{key}={value}\n")
        file.truncate()


def create_s3_bucket(bucket_name):
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"S3 bucket '{bucket_name}' created successfully.")
        update_env_file("BUCKET_NAME", bucket_name)
    except Exception as e:
        print(f"Error creating S3 bucket: {e}")


def create_dynamodb_table(table_name):
    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'ID', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'ID', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"DynamoDB table '{table_name}' created successfully.")
        update_env_file("DYNAMODB_TABLE_NAME", table_name)
    except Exception as e:
        print(f"Error creating DynamoDB table: {e}")


def create_iam_role(role_name, policy_name):
    try:
        # Define trust relationship for AWS services
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": ["lambda.amazonaws.com", "textract.amazonaws.com"]},
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        # Define policy for S3, Textract, and OpenSearch access
        role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["s3:*", "textract:*", "es:*"],
                    "Resource": "*"
                }
            ]
        }

        # Create the IAM role
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        print(f"IAM Role '{role_name}' created successfully.")
        update_env_file("IAM_ROLE_NAME", role_name)

        # Attach policy to the role
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(role_policy)
        )
        print(f"Policy '{policy_name}' attached to IAM Role '{role_name}'.")
        update_env_file("IAM_POLICY_NAME", policy_name)
    except Exception as e:
        print(f"Error creating IAM role: {e}")


def create_opensearch_domain(domain_name):
    try:
        opensearch.create_domain(
            DomainName=domain_name,
            ElasticsearchVersion="OpenSearch_1.0",
            ElasticsearchClusterConfig={
                'InstanceType': 't2.small.elasticsearch',
                'InstanceCount': 1
            },
            EBSOptions={'EBSEnabled': True, 'VolumeSize': 10},
            AccessPolicies=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "es:*",
                        "Resource": f"arn:aws:es:{region}:*:domain/{domain_name}/*"
                    }
                ]
            })
        )
        print(f"OpenSearch domain '{domain_name}' created successfully.")
        update_env_file("OPENSEARCH_DOMAIN_NAME", domain_name)
    except Exception as e:
        print(f"Error creating OpenSearch domain: {e}")


def create_rds_instance(db_identifier, db_name, master_user, master_password):
    try:
        rds.create_db_instance(
            DBInstanceIdentifier=db_identifier,
            AllocatedStorage=20,
            DBInstanceClass='db.t2.micro',
            Engine='mysql',
            MasterUsername=master_user,
            MasterUserPassword=master_password,
            DBName=db_name,
            BackupRetentionPeriod=7
        )
        print(f"RDS instance '{db_identifier}' created successfully.")
        update_env_file("RDS_INSTANCE_ID", db_identifier)
        update_env_file("RDS_DB_NAME", db_name)
        update_env_file("RDS_USER", master_user)
    except Exception as e:
        print(f"Error creating RDS instance: {e}")


if __name__ == "__main__":
    # Retrieve resource names and sensitive info from .env
    bucket_name = os.getenv("BUCKET_NAME", "default-bucket-name")
    dynamodb_table_name = os.getenv("DYNAMODB_TABLE_NAME", "default-table-name")
    iam_role_name = os.getenv("IAM_ROLE_NAME", "default-role-name")
    iam_policy_name = os.getenv("IAM_POLICY_NAME", "default-policy-name")
    opensearch_domain_name = os.getenv("OPENSEARCH_DOMAIN_NAME", "default-domain-name")
    rds_instance_id = os.getenv("RDS_INSTANCE_ID", "default-rds-id")
    rds_db_name = os.getenv("RDS_DB_NAME", "default-db-name")
    rds_user = os.getenv("RDS_USER", "default-user")
    rds_password = os.getenv("RDS_PASSWORD", "default-password")

    # Create resources
    create_s3_bucket(bucket_name)
    create_dynamodb_table(dynamodb_table_name)
    create_iam_role(iam_role_name, iam_policy_name)
    create_opensearch_domain(opensearch_domain_name)
    create_rds_instance(rds_instance_id, rds_db_name, rds_user, rds_password)
