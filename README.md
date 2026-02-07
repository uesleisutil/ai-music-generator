# 🎵 AI Music Generator - AWS Cloud

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-orange.svg)](https://aws.amazon.com/)

Generate professional AI music videos in the cloud with NVIDIA GPUs.

**Cost**: ~$0.02/video | **Speed**: 2-3 min | **Deploy**: Automatic

---

## 🚀 Quick Start

### 1. Get AWS Keys (5 min)

1. AWS Console > IAM > Users > Create user (`github-actions`)
2. Add 6 policies (Batch, ECR, S3, IAM, EC2, Logs)
3. Create access key > Copy both keys

### 2. Configure GitHub Secrets (2 min)

`Settings > Secrets and variables > Actions`

Add:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### 3. Deploy (1 click)

`Actions > Deploy to AWS > Run workflow`

Wait ~15 minutes.

### 4. Test (1 click)

`Actions > Test Deployment > Run workflow`

Download from Artifacts.

📖 **Full guide**: [QUICK_SETUP.md](QUICK_SETUP.md)

---

## 💰 Pricing

| Usage | Monthly Cost |
|-------|--------------|
| 10 videos/day | ~$6 |
| 50 videos/day | ~$29 |
| 100 videos/day | ~$58 |

**Per video**: ~$0.02

---

## 🎯 Features

- 🎵 **MusicGen** (Meta) - AI music generation
- 🎨 **Stable Diffusion** - Lofi/anime style covers
- 🎬 **FFmpeg** - Video creation
- ☁️ **AWS Batch** - GPU acceleration (NVIDIA T4)
- 🤖 **GitHub Actions** - Automatic CI/CD
- 📦 **S3** - Auto-generated bucket name

---

## 📊 Available Models

### Music (7 models)
- musicgen-small (300MB)
- musicgen-medium (1.5GB) ⭐
- musicgen-large (3.3GB)
- audioldm, riffusion, etc.

### Image (6 models)
- sd-2-1 (5GB) ⭐
- sd-xl-base (7GB)
- kandinsky, wuerstchen, etc.

### Presets
- `quick` - Fast
- `balanced` - Recommended ⭐
- `quality` - Best quality
- `experimental` - Unique styles

---

## 🎨 Usage

### Via GitHub Actions
`Actions > Test Deployment > Run workflow`

### Via CLI
```bash
pip install -r requirements-aws.txt

python aws_submit_job.py \
  --prompt "cozy lofi coffee shop music" \
  --duration 60 \
  --preset balanced \
  --output-bucket YOUR-BUCKET-NAME \
  --wait
```

Bucket name is shown in deployment summary.

---

## 📚 Documentation

- [QUICK_SETUP.md](QUICK_SETUP.md) - Setup guide
- [docs/AWS_SETUP.md](docs/AWS_SETUP.md) - Manual deployment
- [docs/AWS_PRICING.md](docs/AWS_PRICING.md) - Cost analysis
- [docs/AI_SETUP.md](docs/AI_SETUP.md) - Models guide

---

## 🛠️ Manual Deployment

```bash
# Install tools
brew install awscli terraform docker

# Deploy
cd terraform
terraform init
terraform apply

# Build & push
./scripts/build_and_push.sh
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 📄 License

MIT - see [LICENSE](LICENSE)

---

**Made with ❤️ and AWS**
