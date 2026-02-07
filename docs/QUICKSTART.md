# ⚡ Quick Start - AWS Cloud

Get your first AI-generated music video in 15 minutes!

---

## 📋 Prerequisites

### 1. AWS Account
- Active AWS account with billing enabled
- IAM user with administrator access

### 2. Install Tools

```bash
# AWS CLI
brew install awscli  # macOS
# or: https://aws.amazon.com/cli/

# Configure AWS
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Format (json)

# Terraform
brew install terraform  # macOS
# or: https://www.terraform.io/downloads

# Docker Desktop
# Download: https://www.docker.com/products/docker-desktop
```

---

## 🚀 Setup (15 minutes)

### Step 1: Clone and Configure (2 min)

```bash
# Clone repository
git clone https://github.com/uesleisutil/ai-music-generator.git
cd ai-music-generator

# Configure Terraform
cd terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

**Important**: Change `s3_bucket_name` to something unique:
```hcl
s3_bucket_name = "your-name-ai-music-2026"  # Must be globally unique!
```

### Step 2: Deploy Infrastructure (5 min)

```bash
cd ..
chmod +x scripts/deploy_aws.sh
./scripts/deploy_aws.sh
```

Type `yes` when prompted. This creates:
- ✅ S3 bucket for outputs
- ✅ ECR repository for Docker images
- ✅ AWS Batch compute environment (GPU Spot instances)
- ✅ Job queue and definition
- ✅ IAM roles and CloudWatch logs

### Step 3: Build Docker Image (10 min - one time)

```bash
chmod +x scripts/build_and_push.sh
./scripts/build_and_push.sh
```

This builds the Docker image with all AI models and pushes to ECR.

### Step 4: Install Python Dependencies (1 min)

```bash
pip install -r requirements-aws.txt
```

---

## 🎵 Generate Your First Video (3 min)

```bash
python aws_submit_job.py \
  --prompt "cozy lofi coffee shop music" \
  --duration 60 \
  --preset balanced \
  --output-bucket your-name-ai-music-2026 \
  --wait
```

The `--wait` flag makes it wait for completion and show the results.

---

## 📥 Download Results

```bash
# List outputs
aws s3 ls s3://your-bucket-name/output/

# Download latest video
aws s3 cp s3://your-bucket-name/output/20260207_123456/video.mp4 ./my-video.mp4

# Download all files from a job
aws s3 sync s3://your-bucket-name/output/20260207_123456/ ./downloads/
```

---

## 🎯 More Examples

### Different Styles

```bash
# Night city
python aws_submit_job.py \
  --prompt "rainy night city with neon lights" \
  --duration 60 \
  --output-bucket your-bucket-name

# Nature
python aws_submit_job.py \
  --prompt "peaceful forest with sunlight" \
  --duration 45 \
  --output-bucket your-bucket-name

# Bedroom
python aws_submit_job.py \
  --prompt "bedroom with city view lofi" \
  --duration 90 \
  --output-bucket your-bucket-name
```

### Batch Generation

```bash
# Edit examples/batch_generate.py with your prompts
nano examples/batch_generate.py  # Change OUTPUT_BUCKET

# Run batch
python examples/batch_generate.py
```

### Different Quality

```bash
# Quick (faster, smaller models)
python aws_submit_job.py \
  --prompt "test" \
  --preset quick \
  --duration 30 \
  --output-bucket your-bucket-name

# Maximum quality (slower, larger models)
python aws_submit_job.py \
  --prompt "jazz lofi" \
  --preset quality \
  --duration 60 \
  --output-bucket your-bucket-name
```

---

## 📊 Monitor Jobs

```bash
# Check running jobs
aws batch list-jobs --job-queue ai-music-generator-queue --job-status RUNNING

# Check completed jobs
aws batch list-jobs --job-queue ai-music-generator-queue --job-status SUCCEEDED

# View logs (real-time)
aws logs tail /aws/batch/ai-music-generator --follow

# Check specific job
aws batch describe-jobs --jobs JOB_ID
```

---

## 💰 Cost Management

### Check Current Spending

```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-02-01,End=2026-02-28 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### Stop Accepting New Jobs

```bash
aws batch update-job-queue \
  --job-queue ai-music-generator-queue \
  --state DISABLED
```

### Delete Everything

```bash
cd terraform
terraform destroy
```

---

## 🐛 Troubleshooting

### "Bucket already exists"
S3 bucket names are globally unique. Change `s3_bucket_name` in `terraform/terraform.tfvars`.

### Job stuck in RUNNABLE
Wait 2-3 minutes for EC2 instances to launch. First job takes longer.

### Job failed
Check logs:
```bash
aws logs tail /aws/batch/ai-music-generator --follow
```

### AWS CLI not configured
```bash
aws configure
```

---

## 📚 Next Steps

- 📖 [Complete AWS Setup Guide](AWS_SETUP.md)
- 💰 [Pricing Analysis](AWS_PRICING.md)
- 🎨 [Models Guide](MODELS.md)
- 🔧 [Advanced Configuration](AWS_SETUP.md#advanced-configuration)

---

## 💡 Tips

1. **First job takes longer**: EC2 instances need to launch (~2-3 min)
2. **Use Spot instances**: Already configured, saves 60-70%
3. **Batch jobs**: Generate multiple videos in one session
4. **Monitor costs**: Set up billing alerts in AWS Console
5. **Clean up**: Delete old S3 outputs regularly

---

**That's it!** You're now generating AI music videos in the cloud! 🎉

**Cost**: ~$0.02 per video | **Speed**: 2-3 minutes | **Quality**: Professional
