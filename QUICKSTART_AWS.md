# ⚡ AWS Quick Start - 5 Minutes to First Video

Get your first AI-generated video running on AWS in 5 minutes!

---

## 🎯 Prerequisites

- AWS account with billing enabled
- AWS CLI installed and configured
- Docker installed
- Terraform installed

**Don't have these?** See [docs/AWS_SETUP.md](docs/AWS_SETUP.md) for installation instructions.

---

## 🚀 5-Minute Setup

### Step 1: Configure (1 minute)

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

Change `s3_bucket_name` to something unique:
```hcl
s3_bucket_name = "your-name-music-gen-2026"
```

### Step 2: Deploy Infrastructure (3 minutes)

```bash
cd ..
chmod +x scripts/deploy_aws.sh
./scripts/deploy_aws.sh
```

Type `yes` when prompted.

### Step 3: Build Docker Image (10 minutes - one time only)

```bash
chmod +x scripts/build_and_push.sh
./scripts/build_and_push.sh
```

### Step 4: Generate Your First Video! (3 minutes)

```bash
python aws_submit_job.py \
  --prompt "cozy lofi coffee shop music" \
  --duration 30 \
  --preset balanced \
  --output-bucket your-name-music-gen-2026 \
  --wait
```

---

## 📥 Download Results

```bash
# List your outputs
aws s3 ls s3://your-bucket-name/output/

# Download latest video
aws s3 cp s3://your-bucket-name/output/LATEST_JOB_ID/video.mp4 ./my-video.mp4
```

---

## 💰 Cost

- First video: ~$0.02
- 10 videos/day: ~$6/month
- 100 videos/day: ~$58/month

---

## 🎉 What's Next?

### Generate More Videos

```bash
# Different styles
python aws_submit_job.py \
  --prompt "rainy night city with neon lights" \
  --duration 60 \
  --output-bucket your-bucket-name

# Batch generation
python examples/batch_generate.py
```

### Monitor Jobs

```bash
# Check status
aws batch list-jobs --job-queue ai-music-generator-queue --job-status RUNNING

# View logs
aws logs tail /aws/batch/ai-music-generator --follow
```

### Stop Spending Money

```bash
# Disable job queue (stops accepting new jobs)
aws batch update-job-queue \
  --job-queue ai-music-generator-queue \
  --state DISABLED
```

---

## 🐛 Troubleshooting

### "Bucket already exists"
Change `s3_bucket_name` in `terraform/terraform.tfvars` to something more unique.

### "No compute capacity"
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

---

## 🗑️ Cleanup

When done testing:

```bash
cd terraform
terraform destroy
```

Type `yes` to delete all resources.

---

## 📚 Full Documentation

- [Complete AWS Setup Guide](docs/AWS_SETUP.md)
- [Pricing Analysis](docs/AWS_PRICING.md)
- [Troubleshooting](docs/AWS_SETUP.md#troubleshooting)

---

**That's it!** You're now generating AI music videos in the cloud! 🎉
