"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Get configuration
config = pulumi.Config()
bucket_name = config.require("bucket_name")
environment = config.require("environment")

# Create an AWS S3 Bucket
bucket = s3.Bucket(
    f'{bucket_name}-bucket',
    bucket=bucket_name,  # Explicit bucket name
    tags={
        "Environment": environment,
        "Project": "pulumi-demo",
        "ManagedBy": "Pulumi",
    }
)

# Export the name of the bucket and ARN
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_arn', bucket.arn)
