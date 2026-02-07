# 🔧 Complete Setup Guide - AWS Cloud

This guide covers the complete setup process for running the AI Music Generator on AWS.

---

## 📋 Prerequisites

### 1. AWS Account Setup

1. **Create AWS Account**: https://aws.amazon.com/
2. **Enable Billing**: Add payment method
3. **Create IAM User** (recommended):
   - Go to IAM Console
   - Create user with `AdministratorAccess` policy
   - Generate Access Key ID and Secret Access Key
   - Save credentials securely

### 2. Install Required Tools

#### AWS CLI

**macOS**:
```bash
brew install awscli
```

**Linux**:
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Windows**:
Download from: https://aws.amazon.com/cli/

**Configure**:
```bash
aws configure
# AWS Access Key ID: YOUR_KEY
# AWS Secret Access Key: YOUR_SECRET
# Default region: us-east-1
# Default output format: json
```

#### Terraform

**macOS**:
```bash
brew install terraform
```

**Linux**:
```bash
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

**Windows**:
Download from: https://www.terraform.io/downloads

**Verify**:
```bash
terraform --version
```

#### Docker

Download Docker Desktop:
- **macOS/Windows**: https://www.docker.com/products/docker-desktop
- **Linux**: https://docs.docker.com/engine/install/

**Verify**:
```bash
docker --version
docker ps
```

---

## 🚀 Deployment

### Step 1: Clone Repository

```bash
git clone https://github.com/uesleisutil/ai-music-generator.git
cd ai-music-generator
```

### Step 2: Configure Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

**Edit these values**:

```hcl
# AWS region (choose closest to you)
aws_region = "us-east-1"  # Options: us-east-1, us-west-2, eu-west-1

# Project name
project_name = "ai-music-generator"

# S3 bucket (MUST BE GLOBALLY UNIQUE!)
s3_bucket_name = "your-unique-name-ai-music-2026"

# ECR repository
ecr_repository_name = "ai-music-generator"
```

**Important**: S3 bucket names must be globally unique. Use your name or company name.

### Step 3: Deploy Infrastructure

```bash
cd ..
chmod +x scripts/deploy_aws.sh
./scripts/deploy_aws.sh
```

This script will:
1. ✅ Validate AWS credentials
2. ✅ Initialize Terraform
3. ✅ Show deployment plan
4. ✅ Ask for confirmation
5. ✅ Create all AWS resources
6. ✅ Save configuration to `aws_config.json`

**Expected time**: 5-10 minutes

**Resources created**:
- S3 bucket for outputs
- ECR repository for Docker images
- AWS Batch compute environment (GPU Spot instances)
- AWS Batch job queue
- AWS Batch job definition
- IAM roles and policies
- Security groups
- CloudWatch log group

### Step 4: Build Docker Image

```bash
chmod +x scripts/build_and_push.sh
./scripts/build_and_push.sh
```

This script will:
1. ✅ Login to ECR
2. ✅ Build Docker image with all dependencies
3. ✅ Tag image
4. ✅ Push to ECR

**Expected time**: 10-15 minutes (first build)

**Image size**: ~15GB (includes PyTorch, CUDA, AI models)

### Step 5: Install Python Dependencies

```bash
pip install -r requirements-aws.txt
```

This installs:
- `boto3` - AWS SDK for Python
- `botocore` - AWS core library

---

## 🎵 Usage

### Submit a Job

```bash
python aws_submit_job.py \
  --prompt "cozy lofi coffee shop music" \
  --duration 60 \
  --preset balanced \
  --output-bucket your-bucket-name \
  --wait
```

**Parameters**:
- `--prompt`: Music description (required)
- `--duration`: Duration in seconds (default: 30)
- `--preset`: Quality preset (quick/balanced/quality/experimental)
- `--output-bucket`: S3 bucket name (required)
- `--output-prefix`: S3 prefix (default: output)
- `--wait`: Wait for job completion (optional)

### Monitor Jobs

```bash
# List running jobs
aws batch list-jobs --job-queue ai-music-generator-queue --job-status RUNNING

# List completed jobs
aws batch list-jobs --job-queue ai-music-generator-queue --job-status SUCCEEDED

# List failed jobs
aws batch list-jobs --job-queue ai-music-generator-queue --job-status FAILED

# Describe specific job
aws batch describe-jobs --jobs JOB_ID

# View logs
aws logs tail /aws/batch/ai-music-generator --follow
```

### Download Results

```bash
# List outputs
aws s3 ls s3://your-bucket-name/output/

# Download specific job
aws s3 sync s3://your-bucket-name/output/20260207_123456/ ./downloads/

# Download just video
aws s3 cp s3://your-bucket-name/output/20260207_123456/video.mp4 ./my-video.mp4
```

---

## 🔧 Advanced Configuration

### Change Instance Types

Edit `terraform/main.tf`:

```hcl
instance_types = [
  "g4dn.xlarge",    # $0.526/hour - 1x NVIDIA T4
  "g4dn.2xlarge",   # $0.752/hour - 1x NVIDIA T4, more RAM
  "g5.xlarge",      # $1.006/hour - 1x NVIDIA A10G (better)
]
```

Apply changes:
```bash
cd terraform
terraform apply
```

### Increase Concurrent Jobs

Edit `terraform/main.tf`:

```hcl
compute_resources {
  max_vcpus = 32  # Increase from 16 (allows 8 concurrent jobs)
}
```

### Use On-Demand Instead of Spot

Edit `terraform/main.tf`:

```hcl
compute_resources {
  type = "EC2"  # Change from "SPOT"
  # Remove: bid_percentage
}
```

**Note**: On-Demand is 2-3x more expensive but never interrupted.

### Change Region

Edit `terraform/terraform.tfvars`:

```hcl
aws_region = "us-west-2"  # Change from us-east-1
```

Redeploy:
```bash
cd terraform
terraform apply
```

---

## 💰 Cost Management

### Set Budget Alerts

1. Go to AWS Billing Console
2. Click "Budgets"
3. Create Budget
4. Set monthly limit (e.g., $50)
5. Add email alerts at 80% and 100%

### Monitor Costs

```bash
# Current month
aws ce get-cost-and-usage \
  --time-period Start=2026-02-01,End=2026-02-28 \
  --granularity MONTHLY \
  --metrics BlendedCost

# By service
aws ce get-cost-and-usage \
  --time-period Start=2026-02-01,End=2026-02-28 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

### Stop Spending

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

## 🗑️ Cleanup

### Delete All Resources

```bash
cd terraform
terraform destroy
```

Type `yes` to confirm.

This will delete:
- ❌ Batch compute environment
- ❌ Batch job queue and definition
- ❌ ECR repository
- ❌ S3 bucket (if empty)
- ❌ IAM roles
- ❌ CloudWatch logs

**Warning**: This is permanent! Download important outputs first.

### Manual Cleanup

If Terraform fails, manually delete:

```bash
# Empty S3 bucket
aws s3 rm s3://your-bucket-name --recursive

# Delete ECR images
aws ecr batch-delete-image \
  --repository-name ai-music-generator \
  --image-ids imageTag=latest

# Then retry terraform destroy
cd terraform
terraform destroy
```

---

## 🐛 Troubleshooting

### AWS CLI not configured
```bash
aws configure
# Enter your credentials
```

### Terraform not found
```bash
# macOS
brew install terraform

# Or download from: https://www.terraform.io/downloads
```

### Docker not running
```bash
# Start Docker Desktop
# Or on Linux:
sudo systemctl start docker
```

### S3 bucket already exists
Change `s3_bucket_name` in `terraform/terraform.tfvars` to something more unique.

### ECR login failed
```bash
# Get AWS account ID
aws sts get-caller-identity

# Login manually
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

### Job stuck in RUNNABLE
Wait 2-3 minutes for EC2 instances to launch. Check:
```bash
aws batch describe-compute-environments \
  --compute-environments ai-music-generator-gpu-spot
```

### Job failed
Check logs:
```bash
aws logs tail /aws/batch/ai-music-generator --follow
```

### Out of memory
Use smaller models:
```bash
python aws_submit_job.py --preset quick --duration 30 --output-bucket your-bucket
```

---

## 📚 Additional Resources

- [AWS Batch Documentation](https://docs.aws.amazon.com/batch/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)
- [Docker Documentation](https://docs.docker.com/)

---

## 💡 Tips

1. **Use Spot Instances**: Already configured, saves 60-70%
2. **Batch Processing**: Generate multiple videos in one session
3. **Monitor Costs**: Set up billing alerts
4. **Clean Up**: Delete old S3 outputs regularly
5. **Regional Selection**: us-east-1 is usually cheapest

---

**Need help?** Open an [issue](https://github.com/uesleisutil/ai-music-generator/issues)!
