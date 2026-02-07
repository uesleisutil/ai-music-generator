# 🔒 Security and Access Control

This document explains how to protect your AWS resources from unauthorized access and prevent unexpected costs.

---

## 🚨 Important: Workflow Access Control

### Current Protection

The **Test Deployment** workflow (`test-deployment.yml`) is protected by:

1. **Environment Protection** - Uses `environment: production`
2. **Secrets Requirement** - Requires AWS credentials (only available to collaborators)
3. **Manual Trigger Only** - Uses `workflow_dispatch` (no automatic runs)

### Who Can Run Test Deployments?

By default, GitHub allows:
- ✅ **Repository Owner** (you)
- ✅ **Collaborators** with write access
- ❌ **External contributors** (cannot access secrets)
- ❌ **Fork repositories** (cannot access secrets)

---

## 🛡️ Additional Protection (Recommended)

### 1. Enable Environment Protection Rules

Go to: `Settings > Environments > production`

**Recommended Settings**:
- ✅ **Required reviewers** - Add yourself as required reviewer
- ✅ **Wait timer** - Add 5-minute delay before deployment
- ✅ **Deployment branches** - Restrict to `main` branch only

**How to Configure**:

1. Go to your repository on GitHub
2. Click **Settings** > **Environments**
3. Click **New environment** or edit **production**
4. Add protection rules:
   ```
   Required reviewers: [your-username]
   Wait timer: 5 minutes (optional)
   Deployment branches: Selected branches > main
   ```

### 2. Restrict Workflow Permissions

Go to: `Settings > Actions > General > Workflow permissions`

**Recommended Settings**:
- ✅ **Read repository contents and packages permissions**
- ❌ **Allow GitHub Actions to create and approve pull requests** (disable)

### 3. Monitor AWS Costs

Set up AWS Budget Alerts:

```bash
# Create a budget alert for $50/month
aws budgets create-budget \
  --account-id YOUR_ACCOUNT_ID \
  --budget file://budget.json
```

**budget.json**:
```json
{
  "BudgetName": "AI-Music-Generator-Monthly",
  "BudgetLimit": {
    "Amount": "50",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST"
}
```

---

## 💰 Cost Protection Strategies

### 1. AWS Batch Compute Environment

The Terraform configuration already includes:
- ✅ **Spot Instances** - 70% cost savings
- ✅ **Auto-scaling to 0** - No idle costs
- ✅ **Max vCPUs limit** - Prevents runaway scaling

### 2. S3 Lifecycle Policies

Add lifecycle rules to automatically delete old videos:

```bash
# Delete videos older than 30 days
aws s3api put-bucket-lifecycle-configuration \
  --bucket YOUR_BUCKET_NAME \
  --lifecycle-configuration file://lifecycle.json
```

**lifecycle.json**:
```json
{
  "Rules": [
    {
      "Id": "DeleteOldVideos",
      "Status": "Enabled",
      "Prefix": "output/",
      "Expiration": {
        "Days": 30
      }
    }
  ]
}
```

### 3. CloudWatch Alarms

Set up alarms for unusual activity:

```bash
# Alert when Batch jobs exceed 10 per hour
aws cloudwatch put-metric-alarm \
  --alarm-name ai-music-high-job-count \
  --alarm-description "Alert when too many jobs are submitted" \
  --metric-name JobsSubmitted \
  --namespace AWS/Batch \
  --statistic Sum \
  --period 3600 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1
```

---

## 🔐 AWS IAM Best Practices

### 1. Least Privilege Access

The GitHub Actions IAM user should have minimal permissions:

**Required Policies**:
- `AmazonEC2ContainerRegistryFullAccess` - For Docker images
- `AmazonS3FullAccess` - For results storage (consider restricting to specific bucket)
- `AWSBatchFullAccess` - For job submission
- `IAMFullAccess` - For Terraform (consider using a separate user)
- `CloudWatchLogsFullAccess` - For monitoring

**Recommended**: Create a custom policy instead of using `*FullAccess`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "batch:SubmitJob",
        "batch:DescribeJobs",
        "batch:ListJobs"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::ai-music-gen-*",
        "arn:aws:s3:::ai-music-gen-*/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    }
  ]
}
```

### 2. Rotate Access Keys

Rotate your AWS access keys regularly:

```bash
# Create new access key
aws iam create-access-key --user-name github-actions

# Update GitHub Secrets with new keys

# Delete old access key
aws iam delete-access-key --user-name github-actions --access-key-id OLD_KEY_ID
```

### 3. Enable MFA

Enable Multi-Factor Authentication for your AWS account:
1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Click your username > Security credentials
3. Assign MFA device

---

## 🚫 What to Avoid

### ❌ Don't Make Repository Public with Secrets

If you make your repository public:
- Remove all AWS credentials from GitHub Secrets
- Use a separate AWS account for public demos
- Consider using AWS Organizations to isolate costs

### ❌ Don't Share AWS Credentials

- Never commit AWS credentials to Git
- Don't share access keys via email/chat
- Use IAM roles instead of access keys when possible

### ❌ Don't Ignore Cost Alerts

- Set up AWS Budget alerts
- Review AWS Cost Explorer monthly
- Monitor CloudWatch metrics

---

## 📊 Monitoring Dashboard

### GitHub Actions

Monitor workflow runs:
- Go to **Actions** tab
- Check **Test Deployment** runs
- Review who triggered each run

### AWS Console

Monitor costs and usage:
- [AWS Cost Explorer](https://console.aws.amazon.com/cost-management/home)
- [AWS Batch Dashboard](https://console.aws.amazon.com/batch/)
- [CloudWatch Logs](https://console.aws.amazon.com/cloudwatch/)

### Cost Breakdown

Expected costs per video:
- Compute (GPU): ~$0.02
- Image (SDXL): ~$0.04
- Storage (S3): ~$0.001
- **Total**: ~$0.06/video

Unexpected costs to watch for:
- ⚠️ Multiple concurrent jobs
- ⚠️ Long-running jobs (>10 min)
- ⚠️ Failed jobs that retry
- ⚠️ Large S3 storage accumulation

---

## 🆘 Emergency: Stop All Jobs

If you see unexpected costs or activity:

### 1. Disable Compute Environment

```bash
# Disable AWS Batch compute environment
aws batch update-compute-environment \
  --compute-environment ai-music-generator-gpu-spot \
  --state DISABLED

# Terminate all running jobs
aws batch terminate-job \
  --job-id JOB_ID \
  --reason "Emergency stop"
```

### 2. Revoke GitHub Actions Access

1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Delete `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
3. This will prevent any new deployments

### 3. Delete AWS Resources

```bash
# Destroy all infrastructure
cd terraform
terraform destroy -auto-approve
```

---

## ✅ Security Checklist

Before making your repository public or adding collaborators:

- [ ] Environment protection rules configured
- [ ] AWS Budget alerts set up ($50/month recommended)
- [ ] CloudWatch alarms configured
- [ ] S3 lifecycle policies enabled (delete after 30 days)
- [ ] IAM user has minimal permissions
- [ ] MFA enabled on AWS account
- [ ] Access keys rotated in last 90 days
- [ ] No AWS credentials in Git history
- [ ] Test deployment workflow requires approval
- [ ] Repository collaborators reviewed

---

## 📞 Support

If you have security concerns:
- 🐛 **Report vulnerabilities**: Use GitHub Security Advisories
- 💬 **Questions**: Open a GitHub Discussion
- 📧 **Private issues**: Contact repository owner directly

---

## 📚 Additional Resources

- [GitHub Actions Security Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Cost Optimization](https://aws.amazon.com/pricing/cost-optimization/)
- [AWS Batch Security](https://docs.aws.amazon.com/batch/latest/userguide/security.html)

---

**Last Updated**: February 2026
