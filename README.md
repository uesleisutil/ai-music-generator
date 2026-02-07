# 🎵 AI Music Generator - AWS Cloud Edition

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-orange.svg)](https://aws.amazon.com/)
[![Deploy](https://github.com/uesleisutil/ai-music-generator/actions/workflows/deploy-aws.yml/badge.svg)](https://github.com/uesleisutil/ai-music-generator/actions/workflows/deploy-aws.yml)

**Generate professional AI music videos in the cloud with NVIDIA GPUs at ~$0.02 per video!**

Complete open-source project to generate music with AI (MusicGen), create artistic covers (Stable Diffusion), and automatically upload to YouTube - all running on AWS Batch with GPU acceleration and automated CI/CD.

---

## ✨ Why AWS Cloud + GitHub Actions?

| Feature | GitHub Actions + AWS | Manual Local |
|---------|---------------------|--------------|
| **Deployment** | ⚡ Automatic CI/CD | 🔧 Manual setup |
| **Speed** | ⚡ 2-3 min/video | 🐌 5-10 min/video |
| **GPU** | ✅ NVIDIA T4 (CUDA) | ❌ Mac ARM incompatible |
| **Cost** | 💰 $0.02/video | 💰 $0 (but slow) |
| **Scalability** | 🚀 Unlimited | 🔒 Limited |
| **Maintenance** | 🤖 Automated | 👨‍💻 Manual |

**Bottom line**: Push to GitHub → Automatic deployment → Generate videos in the cloud!

---

## 🚀 Quick Start (5 minutes)

### Step 1: Fork Repository

```bash
# Fork on GitHub, then clone
git clone https://github.com/YOUR-USERNAME/ai-music-generator.git
cd ai-music-generator
```

### Step 2: Configure GitHub Secrets

Go to **Settings** > **Secrets and variables** > **Actions** and add:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key | `wJalrXUtnFEMI/K7MDENG/...` |
| `S3_BUCKET_NAME` | Unique bucket name | `your-name-ai-music-2026` |

📖 **Detailed guide**: [docs/GITHUB_ACTIONS_SETUP.md](docs/GITHUB_ACTIONS_SETUP.md)

### Step 3: Deploy Automatically

```bash
# Push to main branch
git add .
git commit -m "Initial deployment"
git push origin main
```

**GitHub Actions will automatically**:
1. ✅ Deploy AWS infrastructure (Terraform)
2. ✅ Build Docker image with AI models
3. ✅ Push to Amazon ECR
4. ✅ Update AWS Batch job definition

**Monitor progress**: Go to **Actions** tab in GitHub

### Step 4: Generate Your First Video

After deployment completes (~10-15 min):

```bash
# Install AWS CLI tools
pip install -r requirements-aws.txt

# Submit job
python aws_submit_job.py \
  --prompt "cozy lofi coffee shop music" \
  --duration 60 \
  --preset balanced \
  --output-bucket YOUR-BUCKET-NAME \
  --wait

# Download result
aws s3 cp s3://YOUR-BUCKET-NAME/output/JOB_ID/video.mp4 ./my-video.mp4
```

**Or use GitHub Actions**:
- Go to **Actions** > **Test Deployment** > **Run workflow**
- Enter prompt and settings
- Download results from artifacts

---

## 🎯 GitHub Actions Workflows

### 1. Deploy to AWS (Automatic)

**Trigger**: Push to `main` branch

**What it does**:
- Plans and applies Terraform changes
- Builds and pushes Docker image
- Updates Batch job definition

**Manual trigger**: Actions > Deploy to AWS > Run workflow

### 2. Test Deployment (Manual)

**Trigger**: Manual only

**What it does**:
- Submits test job to AWS Batch
- Waits for completion
- Downloads and uploads results as artifact

**How to use**: Actions > Test Deployment > Run workflow

### 3. Destroy Infrastructure (Manual)

**Trigger**: Manual with confirmation

**What it does**:
- Empties S3 bucket
- Deletes ECR images
- Destroys all AWS resources

**How to use**: Actions > Destroy Infrastructure > Type "destroy"

---

## 💰 Pricing

### AWS Costs (Spot Instances)

| Usage | Monthly Cost | Cost per Video |
|-------|--------------|----------------|
| **10 videos/day** | ~$6/month | $0.02 |
| **50 videos/day** | ~$29/month | $0.02 |
| **100 videos/day** | ~$58/month | $0.02 |

**Breakdown per video**:
- Compute (g4dn.xlarge Spot): $0.017
- Storage (S3): $0.002
- Data transfer: $0.001
- **Total**: ~$0.02

### GitHub Actions

- **2,000 minutes/month** free for public repositories
- **3,000 minutes/month** free for private repositories (Pro)
- Each deployment: ~10-15 minutes
- **Cost**: FREE for most users!

📊 **Full pricing analysis**: [docs/AWS_PRICING.md](docs/AWS_PRICING.md)

---

## 🎨 Usage Examples

### Single Video

```bash
python aws_submit_job.py \
  --prompt "rainy night city with neon lights lofi" \
  --duration 60 \
  --preset balanced \
  --output-bucket your-bucket-name
```

### Batch Generation

```bash
# Edit examples/batch_generate.py with your prompts
python examples/batch_generate.py
```

### Different Quality Presets

```bash
# Quick (faster, smaller models)
--preset quick --duration 30

# Balanced (recommended)
--preset balanced --duration 60

# Quality (best quality)
--preset quality --duration 90
```

### Monitor Jobs

```bash
# Check running jobs
aws batch list-jobs --job-queue ai-music-generator-queue --job-status RUNNING

# View logs
aws logs tail /aws/batch/ai-music-generator --follow

# Download all outputs
aws s3 sync s3://your-bucket-name/output/ ./downloads/
```

---

## 🎨 Prompt Examples

### Cafe/Interior
```
cozy coffee shop with plants and warm lighting, anime style
```

### Night City
```
rainy night city with neon lights and reflections, lofi aesthetic
```

### Bedroom/Study
```
bedroom with city view and desk setup, studio ghibli style
```

### Nature
```
peaceful forest with sunlight through trees, makoto shinkai style
```

---

## 📊 Available Models

### Music Models (7 options)
- **musicgen-small** (300MB) - Fast
- **musicgen-medium** (1.5GB) - ⭐ Recommended
- **musicgen-large** (3.3GB) - Best quality
- **musicgen-melody** (1.5GB) - Melody-focused
- **audioldm** (1.2GB) - Alternative
- **audioldm-large** (2.5GB) - High quality
- **riffusion** (2GB) - Unique style

### Image Models (6 options)
- **sd-2-1** (5GB) - ⭐ Recommended
- **sd-xl-base** (7GB) - Best quality
- **sd-1-5** (4GB) - Lighter
- **kandinsky-2-2** (5GB) - Artistic
- **wuerstchen** (3GB) - Fast
- **deepfloyd-if** (8GB) - Photorealistic

### Presets
- `quick` - musicgen-small + wuerstchen
- `balanced` - musicgen-medium + sd-2-1 ⭐
- `quality` - musicgen-large + sd-xl-base
- `experimental` - riffusion + kandinsky-2-2

---

## 🛠️ Manual Deployment (Alternative)

If you prefer manual deployment without GitHub Actions:

```bash
# Install tools
brew install awscli terraform docker

# Configure AWS
aws configure

# Deploy infrastructure
cd terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars  # Edit s3_bucket_name
terraform init
terraform apply

# Build and push Docker
cd ..
./scripts/build_and_push.sh
```

📖 **Complete manual guide**: [docs/AWS_SETUP.md](docs/AWS_SETUP.md)

---

## 🔧 Configuration

### Change AWS Region

Edit `.github/workflows/deploy-aws.yml`:
```yaml
env:
  AWS_REGION: us-west-2  # Change from us-east-1
```

### Use Different Instance Types

Edit `terraform/main.tf`:
```hcl
instance_types = [
  "g4dn.xlarge",    # $0.526/hour
  "g5.xlarge",      # $1.006/hour - Better GPU
]
```

### Increase Concurrent Jobs

Edit `terraform/main.tf`:
```hcl
compute_resources {
  max_vcpus = 32  # Allows 8 concurrent jobs
}
```

---

## 📚 Documentation

- ⚡ [GitHub Actions Setup](docs/GITHUB_ACTIONS_SETUP.md) ⭐ **NEW**
- 📖 [AWS Setup (Manual)](docs/AWS_SETUP.md)
- 💰 [Pricing Analysis](docs/AWS_PRICING.md)
- 🎨 [Models Guide](docs/AI_SETUP.md)
- 🚀 [Quick Start](docs/QUICKSTART.md)
- 🔧 [Detailed Setup](docs/SETUP.md)

---

## 🐛 Troubleshooting

### GitHub Actions fails

**Check**:
1. GitHub secrets are set correctly
2. IAM user has required permissions
3. S3 bucket name is unique

**View logs**: Actions > [Workflow] > [Job] > [Step]

### Job stuck in RUNNABLE

Wait 2-3 minutes for EC2 instances to launch.

### Job failed

```bash
aws logs tail /aws/batch/ai-music-generator --follow
```

### Bucket name already exists

Change `S3_BUCKET_NAME` secret to something more unique.

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md).

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [MusicGen](https://github.com/facebookresearch/audiocraft) by Meta
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) by Stability AI
- [AWS Batch](https://aws.amazon.com/batch/)
- [GitHub Actions](https://github.com/features/actions)
- [FFmpeg](https://ffmpeg.org/)

---

## 💡 Why This Project?

**Problem**: Mac ARM (Apple Silicon) doesn't support MusicGen GPU acceleration. Local generation takes 5-10 minutes per video.

**Solution**: Automated CI/CD pipeline that deploys to AWS with NVIDIA GPUs for 3-5x faster generation at minimal cost.

**Result**: Push to GitHub → Automatic deployment → Professional AI music videos in 2-3 minutes!

---

## ⭐ Star History

If this project helped you, give it a star! ⭐

---

## 📧 Contact

Questions? Open an [issue](https://github.com/uesleisutil/ai-music-generator/issues)!

---

**Made with ❤️, AWS, and GitHub Actions**

**Cost**: ~$0.02 per video | **Speed**: 2-3 minutes | **Quality**: Professional | **Deployment**: Automatic
