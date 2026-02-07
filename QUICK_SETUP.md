# ⚡ Quick Setup

## 🔑 Step 1: Get AWS Keys (5 min)

1. Go to https://console.aws.amazon.com/iam/
2. **Users** > **Create user**
   - Name: `github-actions`
3. **Attach policies directly**, select:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonS3FullAccess`
   - `AWSBatchFullAccess`
   - `IAMFullAccess`
   - `CloudWatchLogsFullAccess`
   - `AmazonEC2FullAccess`
4. **Create user**
5. Click the user > **Security credentials** > **Create access key**
6. Select: **Application running outside AWS**
7. **Create access key**
8. ⚠️ **Copy both keys NOW** (you won't see them again!)

## 🔐 Step 2: Configure GitHub Secrets (2 min)

Go to: `Settings > Secrets and variables > Actions`

Add 2 secrets:

| Name | Value |
|------|-------|
| `AWS_ACCESS_KEY_ID` | Your Access Key ID |
| `AWS_SECRET_ACCESS_KEY` | Your Secret Access Key |

**That's it!** S3 bucket is auto-generated.

## 🚀 Step 3: Deploy (1 click)

`Actions > Deploy to AWS > Run workflow`

Wait ~15 minutes. Done!

## 🎵 Step 4: Test (1 click)

`Actions > Test Deployment > Run workflow`

Download video from Artifacts.

---

**Cost**: ~$0.02/video | **Time**: 2-3 min/video
