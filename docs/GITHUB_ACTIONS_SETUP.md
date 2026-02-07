# 🚀 GitHub Actions Setup Guide

This guide explains how to set up GitHub Actions for automatic deployment to AWS.

---

## 📋 Prerequisites

1. **AWS Account** with billing enabled
2. **GitHub Repository** with this code
3. **IAM User** with appropriate permissions

---

## 🔐 Step 1: Create IAM User for GitHub Actions

### 1.1 Create IAM User

```bash
# Login to AWS Console
# Go to IAM > Users > Create User

# User name: github-actions-ai-music-generator
# Access type: Programmatic access
```

### 1.2 Attach Policies

Attach these AWS managed policies:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonS3FullAccess`
- `AWSBatchFullAccess`
- `IAMFullAccess`
- `CloudWatchLogsFullAccess`

Or create a custom policy with minimal permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "batch:*",
        "ecr:*",
        "s3:*",
        "iam:*",
        "ec2:*",
        "logs:*",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

### 1.3 Save Credentials

After creating the user, save:
- **Access Key ID**: `AKIAIOSFODNN7EXAMPLE`
- **Secret Access Key**: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

⚠️ **Important**: Save these credentials securely! You won't be able to see the secret key again.

---

## 🔑 Step 2: Configure GitHub Secrets

### 2.1 Go to Repository Settings

1. Go to your GitHub repository
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**

### 2.2 Add Required Secrets

Add these 3 secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `AWS_ACCESS_KEY_ID` | Your IAM user access key | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Your IAM user secret key | `wJalrXUtnFEMI/K7MDENG/...` |
| `S3_BUCKET_NAME` | Unique S3 bucket name | `your-name-ai-music-2026` |

**Important**: The S3 bucket name must be globally unique!

---

## 🎯 Step 3: Configure Terraform Backend (Optional)

For production, use remote state storage:

### 3.1 Create S3 Bucket for Terraform State

```bash
aws s3 mb s3://your-terraform-state-bucket
aws s3api put-bucket-versioning \
  --bucket your-terraform-state-bucket \
  --versioning-configuration Status=Enabled
```

### 3.2 Create DynamoDB Table for State Locking

```bash
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### 3.3 Update terraform/main.tf

Add backend configuration:

```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "ai-music-generator/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

---

## 🚀 Step 4: Deploy to AWS

### 4.1 Push to Main Branch

```bash
git add .
git commit -m "Setup GitHub Actions deployment"
git push origin main
```

This will automatically trigger the deployment workflow!

### 4.2 Monitor Deployment

1. Go to **Actions** tab in GitHub
2. Click on the running workflow
3. Watch the deployment progress

**Expected time**: 10-15 minutes for first deployment

---

## 📊 Available Workflows

### 1. Deploy to AWS (Automatic)

**Trigger**: Push to `main` branch or manual trigger

**What it does**:
1. ✅ Plans Terraform changes
2. ✅ Applies infrastructure changes
3. ✅ Builds Docker image
4. ✅ Pushes to ECR
5. ✅ Updates Batch job definition

**Manual trigger**:
```
Actions > Deploy to AWS > Run workflow
```

### 2. Test Deployment (Manual)

**Trigger**: Manual only

**What it does**:
1. ✅ Submits a test job to AWS Batch
2. ✅ Waits for completion
3. ✅ Downloads results
4. ✅ Uploads as GitHub artifact

**How to run**:
```
Actions > Test Deployment > Run workflow
- Prompt: "cozy lofi coffee shop music"
- Duration: 30
- Preset: balanced
```

### 3. Destroy Infrastructure (Manual)

**Trigger**: Manual only (requires confirmation)

**What it does**:
1. ✅ Empties S3 bucket
2. ✅ Deletes ECR images
3. ✅ Destroys all Terraform resources

**How to run**:
```
Actions > Destroy Infrastructure > Run workflow
- Confirm: type "destroy"
```

⚠️ **Warning**: This is permanent and cannot be undone!

---

## 🔧 Workflow Configuration

### Environment Variables

Edit `.github/workflows/deploy-aws.yml`:

```yaml
env:
  AWS_REGION: us-east-1  # Change if needed
  ECR_REPOSITORY: ai-music-generator
  TERRAFORM_VERSION: 1.6.0
```

### Terraform Variables

The workflow automatically passes:
- `s3_bucket_name` from GitHub secret
- Other variables use defaults from `terraform/main.tf`

To override other variables, edit the workflow:

```yaml
- name: Terraform Plan
  run: |
    terraform plan \
      -var="s3_bucket_name=${{ secrets.S3_BUCKET_NAME }}" \
      -var="aws_region=us-west-2" \
      -var="project_name=my-custom-name"
```

---

## 🐛 Troubleshooting

### Workflow fails at Terraform Plan

**Cause**: Missing or invalid AWS credentials

**Solution**:
1. Check GitHub secrets are set correctly
2. Verify IAM user has required permissions
3. Check AWS region is correct

### Workflow fails at Docker Build

**Cause**: ECR repository doesn't exist

**Solution**:
1. Run Terraform Apply first
2. Or create ECR repository manually:
```bash
aws ecr create-repository --repository-name ai-music-generator
```

### Workflow fails at Terraform Apply

**Cause**: S3 bucket name already exists

**Solution**:
1. Change `S3_BUCKET_NAME` secret to a unique name
2. Re-run workflow

### Test job fails

**Cause**: Infrastructure not deployed or job definition outdated

**Solution**:
1. Run "Deploy to AWS" workflow first
2. Wait for deployment to complete
3. Then run "Test Deployment"

---

## 📊 Monitoring

### View Logs

**GitHub Actions logs**:
```
Actions > [Workflow name] > [Job name] > [Step name]
```

**AWS Batch logs**:
```bash
aws logs tail /aws/batch/ai-music-generator --follow
```

**CloudWatch Console**:
```
https://console.aws.amazon.com/cloudwatch/home#logsV2:log-groups/log-group/$252Faws$252Fbatch$252Fai-music-generator
```

### Check Costs

```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-02-01,End=2026-02-28 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

Or use AWS Cost Explorer in the console.

---

## 🔒 Security Best Practices

### 1. Use Least Privilege IAM Policies

Don't use `AdministratorAccess`. Create custom policies with only required permissions.

### 2. Rotate Access Keys Regularly

```bash
# Create new key
aws iam create-access-key --user-name github-actions-ai-music-generator

# Update GitHub secrets
# Delete old key
aws iam delete-access-key --access-key-id OLD_KEY_ID --user-name github-actions-ai-music-generator
```

### 3. Enable MFA for IAM User

Even for programmatic access users, enable MFA for console access.

### 4. Use Branch Protection

Protect `main` branch:
```
Settings > Branches > Add rule
- Require pull request reviews
- Require status checks to pass
```

### 5. Review Workflow Runs

Regularly check Actions tab for:
- Failed deployments
- Unusual activity
- Cost spikes

---

## 💰 Cost Management

### Set Budget Alerts

1. Go to AWS Billing Console
2. Create Budget
3. Set monthly limit (e.g., $50)
4. Add email alerts at 80% and 100%

### Auto-Stop on Budget Exceeded

Add to workflow:

```yaml
- name: Check Budget
  run: |
    CURRENT_COST=$(aws ce get-cost-and-usage ...)
    if [ $CURRENT_COST -gt $BUDGET_LIMIT ]; then
      echo "Budget exceeded! Stopping deployment."
      exit 1
    fi
```

---

## 🎯 Next Steps

1. ✅ Configure GitHub secrets
2. ✅ Push to main branch
3. ✅ Monitor deployment in Actions tab
4. ✅ Run test deployment
5. ✅ Generate your first video!

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS Batch Documentation](https://docs.aws.amazon.com/batch/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [GitHub Actions for AWS](https://github.com/aws-actions)

---

**Need help?** Open an [issue](https://github.com/uesleisutil/ai-music-generator/issues)!
