# 🛠️ Scripts

Utility scripts for managing the AI Music Generator infrastructure.

---

## 📋 Available Scripts

### 1. `warm_up_gpu.py` 🔥 (Performance Optimization)

Python script to warm up GPU instance before submitting jobs. Keeps instance running for specified duration (default: 60 minutes), then automatically scales down.

**Why use this:**
- First job takes 5-10 minutes (GPU provisioning + Docker download)
- With warm-up, jobs start immediately
- Auto-scales down after duration to save costs

**Usage:**
```bash
# Warm up for 1 hour (default)
python scripts/warm_up_gpu.py

# Warm up for 30 minutes
python scripts/warm_up_gpu.py --duration 30

# Custom settings
python scripts/warm_up_gpu.py --duration 60 --profile b3tr --region us-east-1
```

**Workflow:**
1. Run warm-up before your work session
2. Submit jobs while instance is warm (fast!)
3. Instance auto-scales down after duration
4. Or press Ctrl+C to scale down immediately

**Cost:** g4dn.xlarge Spot ~$0.16/hour (1 hour = ~$0.16)

---

### 2. `setup_cost_alerts.py` ⭐ (Recommended)

Python script to create AWS budget alerts at R$5 increments.

**What it does:**
- Creates SNS topic for notifications
- Subscribes your email to alerts
- Creates 5 budget alerts: $1, $5, $10, $20, $50 USD
- Sends alerts at 80% and 100% of each threshold
- Includes forecasted cost alerts

**Usage:**
```bash
# Install AWS SDK
pip install boto3

# Run the script
python scripts/setup_cost_alerts.py

# Follow the prompts:
# 1. Enter your email
# 2. Confirm the subscription email
# 3. Done!
```

**Budget Alerts Created:**
- 💵 **$1 USD (~R$5)** - Alert at $0.80 and $1.00
- 💵 **$5 USD (~R$25)** - Alert at $4.00 and $5.00
- 💵 **$10 USD (~R$50)** - Alert at $8.00 and $10.00
- 💵 **$20 USD (~R$100)** - Alert at $16.00 and $20.00
- 💵 **$50 USD (~R$250)** - Alert at $40.00 and $50.00

**Email Notifications:**
You'll receive emails when:
- ✅ 80% of budget is reached (warning)
- ✅ 100% of budget is reached (critical)
- ✅ Forecasted to exceed budget (prediction)

---

### 2. `setup_cost_alerts.sh`

Bash script alternative (requires `aws` CLI).

**Usage:**
```bash
# Make executable
chmod +x scripts/setup_cost_alerts.sh

# Run
./scripts/setup_cost_alerts.sh
```

---

### 3. `build_and_push.sh`

Build Docker image and push to AWS ECR.

**Usage:**
```bash
# Make executable
chmod +x scripts/build_and_push.sh

# Run
./scripts/build_and_push.sh
```

**What it does:**
1. Gets AWS account ID
2. Logs in to ECR
3. Builds Docker image with CUDA support
4. Tags image with commit SHA
5. Pushes to ECR repository

**Requirements:**
- Docker installed
- AWS credentials configured
- ECR repository created (by Terraform)

---

### 4. `deploy_aws.sh`

Manual deployment script (alternative to GitHub Actions).

**Usage:**
```bash
# Make executable
chmod +x scripts/deploy_aws.sh

# Run
./scripts/deploy_aws.sh
```

**What it does:**
1. Checks AWS credentials
2. Runs Terraform init
3. Runs Terraform plan
4. Runs Terraform apply
5. Builds and pushes Docker image
6. Displays infrastructure outputs

**Requirements:**
- Terraform installed
- AWS credentials configured
- Docker installed

---

## 🚀 Quick Start

### Setup Cost Alerts (Recommended First Step)

```bash
# 1. Install dependencies
pip install boto3

# 2. Configure AWS credentials (if not already done)
aws configure --profile b3tr

# 3. Run cost alerts setup
python scripts/setup_cost_alerts.py

# 4. Check your email and confirm subscription
```

### Deploy Infrastructure

```bash
# Option 1: Using GitHub Actions (recommended)
# Go to Actions > Deploy to AWS > Run workflow

# Option 2: Manual deployment
./scripts/deploy_aws.sh
```

### Build and Push Docker Image

```bash
# This is usually done by GitHub Actions, but you can run manually:
./scripts/build_and_push.sh
```

---

## 📊 Monitoring Costs

After setting up alerts, monitor your costs:

### AWS Console
- **Budgets**: https://console.aws.amazon.com/billing/home#/budgets
- **Cost Explorer**: https://console.aws.amazon.com/cost-management/home
- **Billing Dashboard**: https://console.aws.amazon.com/billing/home

### Command Line
```bash
# View current month costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -u +%Y-%m-01),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost

# List all budgets
aws budgets describe-budgets \
  --account-id $(aws sts get-caller-identity --query Account --output text)
```

---

## 🔧 Troubleshooting

### Cost Alerts Script Fails

**Error: "AccessDeniedException"**
```bash
# Solution: Add Budgets permissions to your IAM user
aws iam attach-user-policy \
  --user-name github-actions \
  --policy-arn arn:aws:iam::aws:policy/AWSBudgetsActionsWithAWSResourceControlAccess
```

**Error: "Email not confirmed"**
- Check your email inbox (and spam folder)
- Click the confirmation link from AWS SNS
- Re-run the script if needed

### Build Script Fails

**Error: "Cannot connect to Docker daemon"**
```bash
# Solution: Start Docker
# macOS: Open Docker Desktop
# Linux: sudo systemctl start docker
```

**Error: "No such repository"**
```bash
# Solution: Deploy infrastructure first
cd terraform
terraform init
terraform apply
```

### Deploy Script Fails

**Error: "Terraform not found"**
```bash
# Solution: Install Terraform
# macOS: brew install terraform
# Linux: https://www.terraform.io/downloads
```

**Error: "AWS credentials not configured"**
```bash
# Solution: Configure AWS CLI
aws configure --profile b3tr
# Enter your AWS Access Key ID and Secret Access Key
```

---

## 📚 Additional Resources

- [AWS Budgets Documentation](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- [AWS Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Docker Documentation](https://docs.docker.com/)

---

## 🆘 Need Help?

- 🐛 **Issues**: [GitHub Issues](https://github.com/uesleisutil/ai-music-generator/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/uesleisutil/ai-music-generator/discussions)
- 📖 **Documentation**: [docs/](../docs/)

---

**Last Updated**: February 2026
