# Pulumi Demo - AWS S3 Bucket

My first Pulumi project for creating an AWS S3 bucket using Python.

## Project Information

- **Project Name:** pulumi-demo-v1
- **Stack:** dev
- **AWS Region:** us-east-1
- **AWS Account:** 821770019153
- **Pulumi Backend:** Local file system (`file://~`)

## Prerequisites

1. **Pulumi CLI** - Already installed ✓
2. **Python 3.9+** - Already installed ✓
3. **AWS Account** - Private AWS account ✓
4. **AWS Credentials** - Configured in `~/.zprofile`

## AWS Credentials Setup

AWS credentials are stored in `~/.zprofile` as environment variables:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

**Load credentials in terminal:**
```bash
source ~/.zprofile
```

**Verify credentials:**
```bash
aws sts get-caller-identity
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

## How Pulumi Stores Your Stack State

Pulumi needs to track the state of your infrastructure to know what resources exist and their current configuration. Since we configured it with `pulumi login --local`, the state is stored **locally on your computer** (not in Pulumi's cloud service).

### State Storage Location

Your stack state is stored in:
```
~/.pulumi/stacks/pulumi-demo-v1/dev.json
```

Breaking this down:
- `~/.pulumi/` - Pulumi's home directory
- `stacks/` - Where all stack state files are stored
- `pulumi-demo-v1/` - Your project name
- `dev.json` - Your stack name (dev)

### What's Stored in the State File

The state file (`dev.json`) contains:
1. **All deployed resources** - URNs, types, and properties of your S3 bucket
2. **Resource outputs** - Values like bucket name and ARN
3. **Configuration** - Stack config and secrets (encrypted with passphrase)
4. **Deployment history** - Timestamps and metadata about deployments
5. **Resource dependencies** - Relationships between resources

### State File Backups

Pulumi automatically creates backups:
- `dev.json` - Current state
- `dev.json.bak` - Previous state (before last operation)
- `dev.json.attrs` - Metadata about current state
- `dev.json.bak.attrs` - Metadata about backup

### Backend Configuration

Your backend is configured in:
```
~/.pulumi/credentials.json
```

Current setting:
```json
{
    "current": "file://~",
    "accessTokens": {
        "file://~": ""
    }
}
```

This tells Pulumi to use the local file system (`file://~`) instead of the Pulumi Cloud service.

### View Your State

```bash
# View stack state file location
ls -la ~/.pulumi/stacks/pulumi-demo-v1/

# Check which backend you're using
cat ~/.pulumi/credentials.json

# View current stack info (from state)
pulumi stack

# Export state as JSON (for backup or inspection)
pulumi stack export > stack-backup.json

# Import state from JSON (restore)
pulumi stack import < stack-backup.json
```

### Important Notes

⚠️ **State File is Critical:**
- Without the state file, Pulumi doesn't know what resources it created
- Always backup `~/.pulumi/stacks/` if backing up your machine
- Don't manually edit the state file (use `pulumi` commands)

⚠️ **Local Backend Limitations:**
- State is only on your computer (not shared with team)
- No state locking (don't run multiple `pulumi up` simultaneously)
- Need to manually backup state files

⚠️ **State File is NOT in Git:**
- The `.gitignore` doesn't exclude state files (they're outside the project)
- State contains sensitive information (resource IDs, configurations)
- For team collaboration, consider using Pulumi Cloud or AWS S3 backend

### Alternative Backends

You can change to other backends later:

**Pulumi Cloud (Free for individuals):**
```bash
pulumi login
```

**AWS S3 Backend:**
```bash
pulumi login s3://my-pulumi-state-bucket
```

**Azure Blob Storage:**
```bash
pulumi login azblob://my-container
```

## Project Setup Commands

```bash
# 1. Configure Pulumi to use local backend (state stored locally)
pulumi login --local

# 2. Create new Pulumi project
pulumi new aws-python --yes --name pulumi-demo-v1 --description "My first Pulumi project - AWS S3 bucket" --stack dev

# 3. Activate Python virtual environment
source venv/bin/activate
```

## Pulumi Commands

### Preview Changes (Dry Run)
Preview what resources will be created without actually deploying:
```bash
pulumi preview
```

### Deploy Infrastructure
Create the S3 bucket in AWS:
```bash
pulumi up
```
- Pulumi will show you the planned changes
- Type `yes` to confirm and deploy
- If prompted for passphrase, press Enter (no passphrase)

### View Stack Outputs
Check the bucket name and ARN after deployment:
```bash
pulumi stack output
pulumi stack output bucket_name
pulumi stack output bucket_arn
```

### View Current Stack Info
```bash
pulumi stack
pulumi stack ls
```

### Refresh State
Sync Pulumi state with actual AWS resources:
```bash
pulumi refresh
```

## How to Delete the Bucket

### Option 1: Using Pulumi (Recommended)
This removes the bucket and cleans up Pulumi state:

```bash
# 1. Make sure you're in the project directory
cd /Users/edim/edi-github/pulumi-demo-v1

# 2. Load AWS credentials
source ~/.zprofile

# 3. Activate virtual environment
source venv/bin/activate

# 4. Destroy the infrastructure
pulumi destroy
```

Pulumi will:
- Show you what will be deleted
- Ask for confirmation (type `yes`)
- Delete the S3 bucket from AWS
- Remove the resources from Pulumi state

### Option 2: Using AWS CLI
Delete the bucket directly using AWS CLI:

```bash
# Delete bucket (must be empty first)
aws s3 rb s3://my-first-bucket-2f3cb75 --force

# Or if bucket has objects, delete all contents first:
aws s3 rm s3://my-first-bucket-2f3cb75 --recursive
aws s3 rb s3://my-first-bucket-2f3cb75
```

**Note:** If you delete via AWS CLI, run `pulumi refresh` to sync Pulumi state.

### Option 3: AWS Console
1. Go to AWS Console → S3
2. Find bucket: `my-first-bucket-2f3cb75`
3. Empty the bucket first (if it contains objects)
4. Click "Delete" and confirm

**Note:** After manual deletion, run `pulumi refresh` to update state.

## Project Structure

```
pulumi-demo-v1/
├── __main__.py           # Main Pulumi program (defines S3 bucket)
├── Pulumi.yaml           # Project configuration
├── Pulumi.dev.yaml       # Stack configuration for 'dev'
├── requirements.txt      # Python dependencies
├── venv/                 # Python virtual environment
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Current Resources

After successful deployment:
- **S3 Bucket:** `my-first-bucket-2f3cb75`
- **Tags:** Environment=Dev, Project=pulumi-demo

## Troubleshooting

### Error: Credentials not found
```bash
# Load AWS credentials
source ~/.zprofile

# Verify
aws sts get-caller-identity
```

### Error: Permission denied (s3:GetBucketPolicy)
Add the missing S3 permissions to your IAM user `edi-pulumi-user`.

### Error: Passphrase required
Press Enter when prompted (we're using no passphrase for this demo).

## Useful Commands

```bash
# List all S3 buckets in your account
aws s3 ls

# Check if the Pulumi bucket exists
aws s3 ls | grep my-first-bucket

# View bucket details
aws s3api get-bucket-location --bucket my-first-bucket-2f3cb75
aws s3api get-bucket-tagging --bucket my-first-bucket-2f3cb75

# View Pulumi state files (local backend)
ls -la ~/.pulumi/
```

## Next Steps

- Modify `__main__.py` to add more AWS resources
- Configure bucket versioning, encryption, or lifecycle policies
- Add S3 objects to the bucket
- Explore other AWS services (EC2, Lambda, RDS, etc.)
- Learn about Pulumi stacks for multi-environment deployments

## Resources

- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Pulumi AWS Provider](https://www.pulumi.com/registry/packages/aws/)
- [Pulumi Python SDK](https://www.pulumi.com/docs/reference/pkg/python/pulumi/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
