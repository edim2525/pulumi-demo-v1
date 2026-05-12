"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Get configuration
config = pulumi.Config()
bucket_name = config.require("bucket_name")
environment = config.require("environment")
additional_buckets = config.get_object("additional_buckets") or []

# Create main S3 Bucket
bucket = s3.Bucket(
    f'{bucket_name}-bucket',
    bucket=bucket_name,  # Explicit bucket name
    tags={
        "Environment": environment,
        "Project": "pulumi-demo",
        "ManagedBy": "Pulumi",
    }
)

# Create additional buckets from config (company pattern)
additional_bucket_resources = []
for additional_bucket_name in additional_buckets:
    additional_bucket = s3.Bucket(
        f'{additional_bucket_name}-bucket',
        bucket=additional_bucket_name,
        tags={
            "Environment": environment,
            "Project": "pulumi-demo",
            "ManagedBy": "Pulumi",
        }
    )
    additional_bucket_resources.append(additional_bucket)

# Export the name of the bucket and ARN
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_arn', bucket.arn)
pulumi.export('additional_buckets', [b.id for b in additional_bucket_resources])
