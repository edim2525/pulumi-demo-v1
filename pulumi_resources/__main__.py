"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Get configuration
config = pulumi.Config()
environment = config.require("environment")
buckets = config.require_object("buckets")  # List of all bucket names

# Create all S3 buckets from config list
created_buckets = []
for bucket_name in buckets:
    bucket = s3.Bucket(
        f'{bucket_name}-bucket',
        bucket=bucket_name,
        tags={
            "Environment": environment,
            "Project": "pulumi-demo",
            "ManagedBy": "Pulumi",
        }
    )
    created_buckets.append(bucket)

# Export bucket information
# First bucket is considered "primary"
pulumi.export('primary_bucket_name', created_buckets[0].id)
pulumi.export('primary_bucket_arn', created_buckets[0].arn)
# Export all bucket names
pulumi.export('all_buckets', [b.id for b in created_buckets])
