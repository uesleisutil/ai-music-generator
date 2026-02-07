# 🚀 AWS Setup Guide - AI Music Generator

This guide will help you deploy the AI Music Generator to AWS Batch with GPU instances.

---

## 📋 Prerequisites

### 1. AWS Account
- Active AWS account with billing enabled
- IAM user with administrator access (or specific permissions)

### 2. Required Tools
```bash
# AWS CLI
brew install awscli  # macOS
# or download from: https://aws.amazon.com/cli/

# Terraform
brew install terraform  # macOS
# or download from: https://www.terraform.io/downloads

# Docker
# Download from: https://www.docker.com/products/docker-desktop
```

### 3. Configure AWS CLI
```bash
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

---

## 🏗️ Deployment Steps

### Step 1: Configure Terraform Variables

```bash
# Copy example configuration
cd terraform
cp terraform.tfvars.example terraform.tfvars

# Edit with your settings
nano terraform.tfvars
```

**Important**: Change `s3_bucket_name` to something unique (S3 bucket names are globally unique):

```hcl
aws_region = "us-east-1"
project_name = "ai-music-generator"
s3_bucket_name = "your-name-ai-music-gen-2026"  # MUST BE UNIQUE!
ecr_repository_name = "ai-music-generator"
```

### Step 2: Deploy Infrastructure

```bash
# Run deployment script
cd ..
chmod +x scripts/deploy_aws.sh
./scripts/deploy_aws.sh
```

This will create:
- ✅ S3 bucket for outputs
- ✅ ECR repository for Docker images
- ✅ AWS Batch compute environment (GPU Spot instances)
- ✅ AWS Batch job queue
- ✅ AWS Batch job definition
- ✅ IAM roles and policies
- ✅ CloudWatch log group

**Expected time**: 5-10 minutes

### Step 3: Build and Push Docker Image

```bash
# Build and push to ECR
chmod +x scripts/build_and_push.sh
./scripts/build_and_push.sh
```

This will:
- ✅ Build Docker image with all dependencies
- ✅ Login to ECR
- ✅ Push image to your ECR repository

**Expected time**: 10-15 minutes (first build)

---

## 🎵 Usage

### Submit a Job

```bash
# Basic usage
python aws_submit_job.py \
  --prompt "cozy lofi coffee shop music" \
  --duration 60 \
  --preset balanced \
  --output-bucket your-bucket-name

# With wait (waits for completion)
python aws_submit_job.py \
  --prompt "peaceful forest ambience" \
  --duration 30 \
  --preset quality \
  --output-bucket your-bucket-name \
  --wait
```

### Check Job Status

```bash
# Using AWS CLI
aws batch describe-jobs --jobs <JOB_ID>

# View logs
aws logs tail /aws/batch/ai-music-generator --follow
```

### Download Results

```bash
# List files
aws s3 ls s3://your-bucket-name/output/

# Download specific job
aws s3 sync s3://your-bucket-name/output/20260207_123456/ ./downloads/

# Download just the video
aws s3 cp s3://your-bucket-name/output/20260207_123456/video.mp4 ./
```

---

## 💰 Cost Management

### Monitor Costs

```bash
# Check current month costs
aws ce get-cost-and-usage \
  --time-period Start=2026-02-01,End=2026-02-28 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### Set Budget Alerts

1. Go to AWS Billing Console
2. Create Budget
3. Set monthly limit (e.g., $50)
4. Add email alerts at 80% and 100%

### Stop All Resources

```bash
# Disable job queue (stops accepting new jobs)
aws batch update-job-queue \
  --job-queue ai-music-generator-queue \
  --state DISABLED

# Set compute environment to 0 instances
aws batch update-compute-environment \
  --compute-environment ai-music-generator-gpu-spot \
  --compute-resources minvCpus=0,maxvCpus=0,desiredvCpus=0
```

---

## 🔧 Advanced Configuration

### Use Different Instance Types

Edit `terraform/main.tf`:

```hcl
instance_types = [
  "g4dn.xlarge",    # $0.526/hour - 1 GPU
  "g4dn.2xlarge",   # $0.752/hour - 1 GPU, more RAM
  "g5.xlarge",      # $1.006/hour - Better GPU
]
```

### Increase Concurrent Jobs

Edit `terraform/main.tf`:

```hcl
compute_resources {
  max_vcpus = 32  # Increase from 16 (allows 8 concurrent jobs)
}
```

### Change to On-Demand Instances

Edit `terraform/main.tf`:

```hcl
compute_resources {
  type = "EC2"  # Change from "SPOT"
  # Remove bid_percentage
}
```

**Note**: On-Demand is 2-3x more expensive but never interrupted.

---

## 🐛 Troubleshooting

### Job Stuck in RUNNABLE

**Cause**: No compute capacity available

**Solution**:
```bash
# Check compute environment
aws batch describe-compute-environments \
  --compute-environments ai-music-generator-gpu-spot

# Check if instances are launching
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=ai-music-generator-batch-instance"
```

### Job Failed

**Check logs**:
```bash
# Get job ID
JOB_ID="your-job-id"

# View logs
aws logs tail /aws/batch/ai-music-generator --follow

# Or in CloudWatch Console:
# https://console.aws.amazon.com/cloudwatch/home#logsV2:log-groups/log-group/$252Faws$252Fbatch$252Fai-music-generator
```

### Out of Memory

**Solution**: Use larger instance type or reduce model size

Edit job submission:
```bash
python aws_submit_job.py \
  --preset quick \  # Uses smaller models
  --duration 30     # Shorter duration
```

### Docker Build Fails

**Common issues**:
- Not enough disk space: Free up space
- Network timeout: Retry build
- CUDA version mismatch: Check Dockerfile base image

---

## 🗑️ Cleanup

### Destroy All Infrastructure

```bash
cd terraform
terraform destroy
```

This will delete:
- ❌ Batch compute environment
- ❌ Batch job queue and definition
- ❌ ECR repository
- ❌ S3 bucket (if empty)
- ❌ IAM roles
- ❌ CloudWatch logs

**Warning**: This is permanent! Download any important outputs first.

### Manual Cleanup

```bash
# Delete S3 bucket contents
aws s3 rm s3://your-bucket-name --recursive

# Delete ECR images
aws ecr batch-delete-image \
  --repository-name ai-music-generator \
  --image-ids imageTag=latest
```

---

## 📊 Monitoring

### CloudWatch Dashboard

Create custom dashboard:
1. Go to CloudWatch Console
2. Create Dashboard
3. Add widgets:
   - Batch job metrics
   - EC2 GPU utilization
   - S3 storage usage
   - Cost metrics

### Useful Metrics

```bash
# Jobs submitted today
aws batch list-jobs \
  --job-queue ai-music-generator-queue \
  --job-status SUCCEEDED

# Current running jobs
aws batch list-jobs \
  --job-queue ai-music-generator-queue \
  --job-status RUNNING

# Failed jobs
aws batch list-jobs \
  --job-queue ai-music-generator-queue \
  --job-status FAILED
```

---

## 🔐 Security Best Practices

### 1. Use IAM Roles (Not Root Account)

```bash
# Create dedicated IAM user
aws iam create-user --user-name ai-music-generator-user

# Attach minimal permissions
aws iam attach-user-policy \
  --user-name ai-music-generator-user \
  --policy-arn arn:aws:iam::aws:policy/AWSBatchFullAccess
```

### 2. Enable S3 Encryption

Add to `terraform/main.tf`:

```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "output_bucket" {
  bucket = aws_s3_bucket.output_bucket.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

### 3. Restrict S3 Access

```hcl
resource "aws_s3_bucket_public_access_block" "output_bucket" {
  bucket = aws_s3_bucket.output_bucket.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

---

## 📚 Additional Resources

- [AWS Batch Documentation](https://docs.aws.amazon.com/batch/)
- [EC2 GPU Instances](https://aws.amazon.com/ec2/instance-types/g4/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Docker Documentation](https://docs.docker.com/)

---

## 💡 Tips

1. **Start Small**: Test with `--preset quick` and short durations first
2. **Use Spot Instances**: Save 60-70% on compute costs
3. **Batch Jobs**: Generate multiple videos in one session
4. **Monitor Costs**: Set up billing alerts
5. **Clean Up**: Delete old outputs from S3 regularly
6. **Regional Selection**: us-east-1 is usually cheapest

---

**Need Help?** Open an issue on GitHub or check the troubleshooting section above.
