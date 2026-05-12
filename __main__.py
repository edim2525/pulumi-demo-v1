"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS S3 Bucket
# Note: AWS will generate a unique name for the bucket
bucket = s3.Bucket(
    'my-first-bucket',
    tags={
        "Environment": "Dev",
        "Project": "pulumi-demo",
    }
)

# Export the name of the bucket so we can see it after deployment
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_arn', bucket.arn)
