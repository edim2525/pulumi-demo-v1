# Pulumi Demo - AWS S3 Bucket

My first Pulumi project for creating AWS S3 buckets using Python with multi-environment support.

## Project Information

- **Project Name:** pulumi-demo-v1
- **Stacks:** dev, prod
- **AWS Region:** us-east-1
- **AWS Account:** 821770019153
- **Pulumi Backend:** Pulumi Cloud (https://app.pulumi.com/edim2525)

## Project Structure

```
pulumi-demo-v1/
├── pulumi_resources/                    # All infrastructure code
│   ├── __main__.py                      # Infrastructure definition
│   ├── Pulumi.yaml                      # Project configuration
│   ├── requirements.txt                 # Python dependencies
│   └── environments/                    # Stack configurations by environment
│       ├── dev/
│       │   └── Pulumi.dev.yaml          # Dev stack configuration
│       └── prod/
│           └── Pulumi.prod.yaml         # Prod stack configuration
├── venv/                                # Python virtual environment
└── README.md
```

**Company-standard structure:**
- Stack configurations are organized in `environments/` subdirectories
- One infrastructure file (`__main__.py`) used by all environments
- Matches company repo pattern at `/Users/edim/skai-github/pulumi-singlestore-provision`

## Current Infrastructure

**Dev Environment:**
- Main Bucket: `edi-pulumi-demo-dev`
- Additional Buckets:
  - `edi-pulumi-demo-dev-logs`
  - `edi-pulumi-demo-dev-backups`
- Tags: Environment=dev, Project=pulumi-demo, ManagedBy=Pulumi
- Stack URL: https://app.pulumi.com/edim2525/pulumi-demo-v1/dev

**Prod Environment:**
- Main Bucket: `edi-pulumi-demo-prod`
- Additional Buckets:
  - `edi-pulumi-demo-prod-logs`
  - `edi-pulumi-demo-prod-backups`
  - `edi-pulumi-demo-prod-archives`
- Tags: Environment=prod, Project=pulumi-demo, ManagedBy=Pulumi
- Stack URL: https://app.pulumi.com/edim2525/pulumi-demo-v1/prod

## Prerequisites

1. **Pulumi CLI** - Already installed ✓
2. **Python 3.9+** - Already installed ✓
3. **AWS Account** - Private AWS account ✓
4. **AWS Credentials** - Configured in `~/.zprofile`
5. **Pulumi Cloud Account** - Logged in as edim2525 ✓

## AWS Credentials Setup

AWS credentials are stored in `~/.zprofile` as environment variables:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"

# Pulumi passphrase (empty for this demo project)
export PULUMI_CONFIG_PASSPHRASE=""
```

**Load credentials in terminal:**
```bash
source ~/.zprofile
```

**Verify credentials:**
```bash
aws sts get-caller-identity
```

## How Pulumi Determines Which AWS Account to Use

Pulumi uses the **AWS SDK** under the hood, which means it follows the same credential resolution process as the AWS CLI and other AWS tools. Here's how Pulumi knows which AWS account to use:

### Credential Resolution Order

Pulumi checks for AWS credentials in the following order:

1. **Environment Variables** (Highest Priority)
   ```bash
   export AWS_ACCESS_KEY_ID="your-access-key"
   export AWS_SECRET_ACCESS_KEY="your-secret-key"
   export AWS_REGION="us-east-1"
   ```
   This is what we're using in this project (stored in `~/.zprofile`)

2. **AWS CLI Configuration Files**
   ```bash
   ~/.aws/credentials  # Credentials file
   ~/.aws/config       # Configuration file with profiles
   ```

3. **IAM Role (for EC2 instances, Lambda, etc.)**
   - Automatically assigned when running on AWS infrastructure
   - Uses instance metadata service

4. **Environment-specific variables**
   - `AWS_PROFILE` - Select a specific AWS CLI profile
   - `AWS_SESSION_TOKEN` - For temporary credentials

### Current Configuration

**This project uses Account:** 821770019153  
**IAM User:** edi-pulumi-user  
**Region:** us-east-1

You can verify which account Pulumi will use:

```bash
# Check current AWS identity
aws sts get-caller-identity

# Output shows:
# {
#     "UserId": "AIDAXXXXXXXXXXXXXXXXX",
#     "Account": "821770019153",
#     "Arn": "arn:aws:iam::821770019153:user/edi-pulumi-user"
# }
```

### Using Different AWS Accounts

If you have multiple AWS accounts (e.g., dev account, prod account), here are your options:

#### Option 1: Use AWS CLI Profiles (Recommended)

**Setup profiles in `~/.aws/credentials`:**
```ini
[default]
aws_access_key_id = YOUR_DEFAULT_KEY
aws_secret_access_key = YOUR_DEFAULT_SECRET

[dev-account]
aws_access_key_id = YOUR_DEV_KEY
aws_secret_access_key = YOUR_DEV_SECRET

[prod-account]
aws_access_key_id = YOUR_PROD_KEY
aws_secret_access_key = YOUR_PROD_SECRET
```

**Use specific profile with Pulumi:**
```bash
# Set profile for dev stack
cd pulumi_resources
export AWS_PROFILE=dev-account
pulumi up

# Set profile for prod stack
cd pulumi_resources
export AWS_PROFILE=prod-account
pulumi up
```

#### Option 2: Configure Profile in Stack Config

You can specify the AWS profile directly in your Pulumi stack configuration:

```bash
# For dev stack
cd pulumi_resources
pulumi config set aws:profile dev-account

# For prod stack
cd pulumi_resources
pulumi config set aws:profile prod-account
```

This stores the profile in `Pulumi.dev.yaml` / `Pulumi.prod.yaml`:
```yaml
config:
  aws:profile: dev-account
  aws:region: us-east-1
  pulumi-demo-v1:bucket_name: edi-pulumi-demo-dev
  pulumi-demo-v1:environment: dev
```

#### Option 3: Set Environment Variables Per Stack

Create environment-specific scripts:

**`dev-env.sh`:**
```bash
#!/bin/bash
export AWS_ACCESS_KEY_ID="dev-account-key"
export AWS_SECRET_ACCESS_KEY="dev-account-secret"
export AWS_REGION="us-east-1"
export PULUMI_CONFIG_PASSPHRASE=""
```

**`prod-env.sh`:**
```bash
#!/bin/bash
export AWS_ACCESS_KEY_ID="prod-account-key"
export AWS_SECRET_ACCESS_KEY="prod-account-secret"
export AWS_REGION="us-east-1"
export PULUMI_CONFIG_PASSPHRASE=""
```

**Usage:**
```bash
# For dev
source dev-env.sh
cd pulumi_resources
pulumi up

# For prod
source prod-env.sh
cd pulumi_resources
pulumi up
```

### Verify Which Account Pulumi Will Use

Before running `pulumi up`, always verify you're using the correct account:

```bash
# Method 1: Check AWS identity
aws sts get-caller-identity

# Method 2: Check Pulumi config
pulumi config

# Method 3: Preview without applying
pulumi preview
# This shows which resources will be affected in which account
```

### How Pulumi Compares Resources

When you run `pulumi up` or `pulumi preview`, Pulumi:

1. **Reads your code** (`__main__.py`) to see what infrastructure you want
2. **Checks its state** (stored in Pulumi Cloud) to see what's currently deployed
3. **Queries AWS** using your credentials to verify actual resources
4. **Compares** the three sources to determine what needs to be created, updated, or deleted

**Example:**
```bash
cd pulumi_resources
pulumi preview

# Pulumi will:
# 1. Read __main__.py and see you want a bucket named "edi-pulumi-demo-dev"
# 2. Check state in Pulumi Cloud for stack "edim2525/pulumi-demo-v1/dev"
# 3. Query AWS account 821770019153 using your credentials
# 4. Compare and show: "no changes required" or "will create/update/delete"
```

### Important Notes

⚠️ **State vs Reality:**
- Pulumi's state tracks what *Pulumi thinks* exists
- AWS has the actual resources
- If someone manually changes resources in AWS Console, Pulumi won't know until you run `pulumi refresh`

⚠️ **Account Isolation:**
- Each AWS account is completely separate
- Resources in account A cannot be seen or modified from account B
- You need separate credentials for each account

⚠️ **Stack and Account Relationship:**
- One Pulumi stack = One set of resources in one AWS account
- You can have `dev` stack pointing to dev AWS account
- And `prod` stack pointing to prod AWS account
- The stack name doesn't automatically determine the AWS account - YOU configure which account via credentials

### Best Practice: Document Your Account Strategy

Add this to your stack configuration or README:

```yaml
# Pulumi.dev.yaml
# This stack deploys to AWS Account: 821770019153 (Dev Account)
# IAM User: edi-pulumi-user-dev
# Region: us-east-1
config:
  aws:region: us-east-1
  pulumi-demo-v1:bucket_name: edi-pulumi-demo-dev
  pulumi-demo-v1:environment: dev
```

## Required IAM Permissions

The IAM user `edi-pulumi-user` needs the following S3 permissions:
- `s3:CreateBucket`, `s3:DeleteBucket`, `s3:ListBucket`
- `s3:GetBucketPolicy`, `s3:PutBucketPolicy`, `s3:DeleteBucketPolicy`
- `s3:GetBucketTagging`, `s3:PutBucketTagging`
- `s3:GetBucketPublicAccessBlock`, `s3:PutBucketPublicAccessBlock`
- `s3:GetBucketAcl`, `s3:GetBucketLocation`, `s3:GetBucketVersioning`
- `s3:ListAllMyBuckets`, `s3:HeadBucket`

**Quick setup:** Attach `AmazonS3FullAccess` managed policy to your IAM user.

## Pulumi Cloud Backend

This project uses **Pulumi Cloud** to store infrastructure state, which provides:

- ✅ **Cloud-based state storage** - Access your state from any machine
- ✅ **State locking** - Prevents concurrent modifications
- ✅ **State history** - View and rollback to previous versions
- ✅ **Team collaboration** - Share stacks with team members
- ✅ **Web dashboard** - View resources at https://app.pulumi.com/edim2525/pulumi-demo-v1

### Login to Pulumi Cloud

```bash
# Login via browser (recommended)
pulumi login

# Or login with access token
pulumi login
# Then paste your token from https://app.pulumi.com/account/tokens

# Verify login
pulumi whoami
# Output: edim2525
```

### View Your Stacks

```bash
# List all stacks
pulumi stack ls

# View stack in browser
pulumi stack --show-urls

# Or visit directly:
# - Dev:  https://app.pulumi.com/edim2525/pulumi-demo-v1/dev
# - Prod: https://app.pulumi.com/edim2525/pulumi-demo-v1/prod
```

## Working with Stacks

All Pulumi operations are run from the `pulumi_resources/` directory. You switch between dev and prod using `pulumi stack select`.

### Working Directory

```bash
# Always work from here
cd pulumi_resources
```

### Work with Dev Environment

```bash
cd pulumi_resources/environments/dev
pulumi config              # View dev configuration
pulumi preview             # Preview dev changes
pulumi up                  # Deploy to dev
```

### Work with Prod Environment

```bash
cd pulumi_resources/environments/prod
pulumi config              # View prod configuration
pulumi preview             # Preview prod changes
pulumi up                  # Deploy to prod
```

### View All Stacks

```bash
cd pulumi_resources/environments/dev  # Or any subdirectory with Pulumi.yaml parent
pulumi stack ls                        # List all stacks and see which is active
```

### How It Works

- **One infrastructure file** (`__main__.py`) is shared by all environments
- **Configuration per environment** (in `environments/dev/` and `environments/prod/`)
- **Navigate to environment directory** and Pulumi automatically uses the right config
- **Same code, different config** = deploy the same infrastructure to different environments with different settings

### View Stack Configuration

```bash
# View config for current stack
pulumi config

# Get specific config value
pulumi config get environment
pulumi config get buckets

# View all stack info
pulumi stack
```

## Managing S3 Buckets

### Clear, Simple Structure

All buckets are defined in a **single list** - no confusing "main" vs "additional" buckets!

**Dev Configuration** (`environments/dev/Pulumi.dev.yaml`):
```yaml
config:
  pulumi-demo-v1:environment: dev
  pulumi-demo-v1:buckets:
    - edi-pulumi-demo-dev
    - edi-pulumi-demo-dev-logs
    - edi-pulumi-demo-dev-backups
  aws:region: us-east-1
```

**Prod Configuration** (`environments/prod/Pulumi.prod.yaml`):
```yaml
config:
  pulumi-demo-v1:environment: prod
  pulumi-demo-v1:buckets:
    - edi-pulumi-demo-prod
    - edi-pulumi-demo-prod-logs
    - edi-pulumi-demo-prod-backups
    - edi-pulumi-demo-prod-archives
  aws:region: us-east-1
```

**Why This Structure?**
- ✅ **Simple**: All buckets in one list
- ✅ **Consistent**: Every bucket is treated the same way
- ✅ **Clear**: No confusion about "main" vs "additional"
- ✅ **Flexible**: Different environments can have different numbers of buckets

### Add More Buckets

**Option 1: Edit the YAML file**
```yaml
config:
  pulumi-demo-v1:environment: dev
  pulumi-demo-v1:buckets:
    - edi-pulumi-demo-dev
    - edi-pulumi-demo-dev-logs
    - edi-pulumi-demo-dev-backups
    - edi-pulumi-demo-dev-new-bucket  # Just add to the list!
  aws:region: us-east-1
```

**Option 2: Use the CLI**
```bash
cd environments/dev
pulumi config set buckets '["edi-pulumi-demo-dev", "edi-pulumi-demo-dev-logs", "edi-pulumi-demo-dev-backups", "edi-pulumi-demo-dev-new-bucket"]'
```

### Preview and Deploy

```bash
cd environments/dev  # or environments/prod
pulumi stack select dev  # or prod

# Preview changes
pulumi preview

# Deploy the new buckets
pulumi up

# Verify in AWS
aws s3 ls | grep edi-pulumi-demo
```

#### 3. Verify Outputs

```bash
# View all stack outputs
pulumi stack output

# View specific output
pulumi stack output backup_bucket_name
pulumi stack output backup_bucket_arn
```

### Add Multiple Buckets with a Loop

If you need to create several similar buckets, use a loop:

```python
"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Get configuration
config = pulumi.Config()
bucket_name = config.require("bucket_name")
environment = config.require("environment")

# Create primary bucket
bucket = s3.Bucket(
    f'{bucket_name}-bucket',
    bucket=bucket_name,
    tags={
        "Environment": environment,
        "Project": "pulumi-demo",
        "ManagedBy": "Pulumi",
    }
)

# Create multiple purpose-specific buckets
bucket_purposes = ["logs", "backups", "uploads", "archives"]
additional_buckets = []

for purpose in bucket_purposes:
    bucket_obj = s3.Bucket(
        f'{bucket_name}-{purpose}-bucket',
        bucket=f"{bucket_name}-{purpose}",
        tags={
            "Environment": environment,
            "Project": "pulumi-demo",
            "ManagedBy": "Pulumi",
            "Purpose": purpose,
        }
    )
    additional_buckets.append(bucket_obj)
    # Export each bucket
    pulumi.export(f'{purpose}_bucket_name', bucket_obj.id)
    pulumi.export(f'{purpose}_bucket_arn', bucket_obj.arn)

# Export primary bucket
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_arn', bucket.arn)
```

This will create:
- `edi-pulumi-demo-dev` (primary)
- `edi-pulumi-demo-dev-logs`
- `edi-pulumi-demo-dev-backups`
- `edi-pulumi-demo-dev-uploads`
- `edi-pulumi-demo-dev-archives`

### Remove a Bucket

To remove a bucket from your infrastructure:

#### 1. Update the Infrastructure Code

Edit `pulumi_resources/__main__.py` and **remove or comment out** the bucket definition:

```python
# # REMOVED: Second bucket no longer needed
# backup_bucket = s3.Bucket(
#     f'{second_bucket_name}-bucket',
#     bucket=second_bucket_name,
#     ...
# )

# Also remove the exports
# pulumi.export('backup_bucket_name', backup_bucket.id)
# pulumi.export('backup_bucket_arn', backup_bucket.arn)
```

#### 2. Preview the Removal

```bash
cd pulumi_resources
pulumi stack select dev  # or prod, depending on which environment
pulumi preview

# You should see: "- aws:s3/bucket:Bucket (delete)"
```

#### 3. Delete the Bucket

```bash
pulumi up

# Pulumi will show the bucket will be deleted
# Type 'yes' to confirm
```

**Important:** The bucket must be **empty** before Pulumi can delete it. If it contains objects:

```bash
# Empty the bucket first
aws s3 rm s3://edi-pulumi-demo-dev-backup --recursive

# Then run pulumi up again
pulumi up
```

#### 4. Verify Removal

```bash
# Check AWS
aws s3 ls | grep edi-pulumi-demo

# Check stack outputs
pulumi stack output
```

### Alternative: Delete Bucket Manually

If you need to delete a bucket without removing it from code:

```bash
# Empty and delete bucket
aws s3 rb s3://edi-pulumi-demo-dev-backup --force

# Refresh Pulumi state to detect the deletion
cd pulumi_resources
pulumi stack select dev  # or prod, depending on which environment
pulumi refresh

# Pulumi will detect the bucket is gone and offer to remove it from state
```

## Common Pulumi Commands

**Important:** Always load your environment variables first:
```bash
source ~/.zprofile  # Loads AWS credentials and Pulumi passphrase
```

### Preview Changes (Dry Run)
```bash
pulumi preview
```

### Deploy Infrastructure
```bash
pulumi up
```

### Destroy All Resources
```bash
pulumi destroy
```

### View Stack Outputs
```bash
pulumi stack output              # All outputs
pulumi stack output bucket_name  # Specific output
```

### View Current Stack Info
```bash
pulumi stack      # Current stack details
pulumi stack ls   # List all stacks
```

### Refresh State
```bash
pulumi refresh    # Sync state with actual AWS resources
```

### View Resource Details
```bash
pulumi stack export | grep -A 10 "aws:s3"  # View S3 resources in state
```

## Verify Your Infrastructure

### Check S3 Buckets

```bash
# List all buckets
aws s3 ls

# List only demo buckets
aws s3 ls | grep edi-pulumi-demo

# View bucket details
aws s3api get-bucket-tagging --bucket edi-pulumi-demo-dev
aws s3api get-bucket-location --bucket edi-pulumi-demo-dev
```

### Check Pulumi Resources

```bash
cd pulumi_resources

# View dev stack resources
pulumi stack select dev
pulumi stack

# View prod stack resources
pulumi stack select prod
pulumi stack

# View in browser
pulumi stack --show-urls
# Or visit: https://app.pulumi.com/edim2525/pulumi-demo-v1/dev (or /prod)
```

## Troubleshooting

### Error: Credentials not found
```bash
# Load AWS credentials
source ~/.zprofile

# Verify
aws sts get-caller-identity
```

### Error: Passphrase must be set
```bash
# Load environment variables (includes passphrase)
source ~/.zprofile

# Or set it manually for current session
export PULUMI_CONFIG_PASSPHRASE=""

# Verify
pulumi stack
```

### Error: Not logged in to Pulumi Cloud
```bash
# Login to Pulumi Cloud
pulumi login

# Verify
pulumi whoami
```

### Error: Permission denied (s3:GetBucketPolicy)
The bucket is created successfully, but Pulumi cannot read the bucket policy due to missing IAM permissions. The bucket works fine; this is just a post-creation verification issue.

**To fix:** Add these permissions to IAM user `edi-pulumi-user`:
- `s3:GetBucketPolicy`
- `s3:PutBucketPolicy`
- `s3:GetBucketVersioning`

### Error: Bucket already exists
```bash
# Check if bucket exists
aws s3 ls | grep your-bucket-name

# Option 1: Use a different bucket name
pulumi config set bucket_name new-unique-bucket-name

# Option 2: Import existing bucket into Pulumi
pulumi import aws:s3/bucket:Bucket my-bucket my-existing-bucket-name
```

## Clean Up

To completely remove all infrastructure:

### Delete Dev Environment
```bash
cd pulumi_resources
pulumi stack select dev
pulumi destroy
```

### Delete Prod Environment
```bash
cd pulumi_resources
pulumi stack select prod
pulumi destroy
```

### Delete Stacks (Optional)
```bash
# Remove dev stack
pulumi stack select dev
pulumi stack rm dev

# Remove prod stack
pulumi stack select prod
pulumi stack rm prod
```

## Next Steps

- **Add more AWS resources:** EC2 instances, Lambda functions, RDS databases
- **Configure bucket policies:** Public access, encryption, versioning
- **Add bucket lifecycle policies:** Transition objects to Glacier
- **Set up bucket notifications:** Trigger Lambda on object uploads
- **Implement infrastructure testing:** Use Pulumi testing framework
- **Add CI/CD pipeline:** Automate deployments with GitHub Actions

## Resources

- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Pulumi AWS Provider](https://www.pulumi.com/registry/packages/aws/)
- [Pulumi Python SDK](https://www.pulumi.com/docs/reference/pkg/python/pulumi/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Pulumi Cloud Dashboard](https://app.pulumi.com/edim2525/pulumi-demo-v1)

## Git Configuration

The repository is configured with SSH key authentication:

```bash
# SSH key location
/Users/edim/keys/edim_github_key

# Git remote
git@github.com:edim2525/pulumi-demo-v1.git
```

## License

This is a personal demo project for learning Pulumi and AWS.
