#!/bin/bash
# Script to check overall project status

AWS_PROFILE=${AWS_PROFILE:-b3tr}
AWS_REGION=${AWS_REGION:-us-east-1}

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        AI Music Generator - Status Check                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check AWS credentials
echo "🔐 AWS Credentials"
if aws sts get-caller-identity --profile $AWS_PROFILE &>/dev/null; then
  ACCOUNT_ID=$(aws sts get-caller-identity --profile $AWS_PROFILE --query Account --output text)
  echo "   ✅ Configured (Account: $ACCOUNT_ID)"
else
  echo "   ❌ Not configured"
  exit 1
fi
echo ""

# Check GPU quota
echo "🎮 GPU Quota"
GPU_QUOTA=$(aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --region $AWS_REGION \
  --profile $AWS_PROFILE \
  --query 'Quota.Value' \
  --output text 2>/dev/null || echo "0")

if [ "$GPU_QUOTA" == "0" ] || [ "$GPU_QUOTA" == "0.0" ]; then
  echo "   ❌ No GPU quota (request increase needed)"
else
  echo "   ✅ $GPU_QUOTA vCPUs available"
fi
echo ""

# Check Batch resources
echo "☁️  AWS Batch"

# Job Queue
if aws batch describe-job-queues --job-queues ai-music-generator-queue --region $AWS_REGION --profile $AWS_PROFILE &>/dev/null; then
  QUEUE_STATUS=$(aws batch describe-job-queues --job-queues ai-music-generator-queue --region $AWS_REGION --profile $AWS_PROFILE --query 'jobQueues[0].state' --output text)
  echo "   ✅ Job Queue: $QUEUE_STATUS"
else
  echo "   ❌ Job Queue: Not found"
fi

# Compute Environment
if aws batch describe-compute-environments --compute-environments ai-music-generator-gpu-ondemand --region $AWS_REGION --profile $AWS_PROFILE &>/dev/null; then
  CE_STATUS=$(aws batch describe-compute-environments --compute-environments ai-music-generator-gpu-ondemand --region $AWS_REGION --profile $AWS_PROFILE --query 'computeEnvironments[0].state' --output text)
  echo "   ✅ Compute Environment: $CE_STATUS"
else
  echo "   ❌ Compute Environment: Not found"
fi
echo ""

# Check S3 buckets
echo "📦 S3 Buckets"
BUCKET_COUNT=$(aws s3 ls --profile $AWS_PROFILE | grep ai-music-gen | wc -l | xargs)
if [ "$BUCKET_COUNT" -gt 0 ]; then
  LATEST_BUCKET=$(aws s3 ls --profile $AWS_PROFILE | grep ai-music-gen | tail -1 | awk '{print $3}')
  echo "   ✅ $BUCKET_COUNT bucket(s) found"
  echo "   📌 Latest: $LATEST_BUCKET"
  
  if [ "$BUCKET_COUNT" -gt 1 ]; then
    echo "   ⚠️  $(($BUCKET_COUNT - 1)) old bucket(s) can be cleaned up"
    echo "      Run: bash scripts/cleanup_s3_buckets.sh"
  fi
else
  echo "   ❌ No buckets found"
fi
echo ""

# Check ECR repository
echo "🐳 Docker Image"
if aws ecr describe-repositories --repository-names ai-music-generator --region $AWS_REGION --profile $AWS_PROFILE &>/dev/null; then
  IMAGE_COUNT=$(aws ecr list-images --repository-name ai-music-generator --region $AWS_REGION --profile $AWS_PROFILE --query 'length(imageIds)' --output text)
  echo "   ✅ ECR Repository exists ($IMAGE_COUNT image(s))"
else
  echo "   ❌ ECR Repository not found"
fi
echo ""

# Check running jobs
echo "🎵 Active Jobs"
RUNNING=$(aws batch list-jobs --job-queue ai-music-generator-queue --job-status RUNNING --region $AWS_REGION --profile $AWS_PROFILE --query 'length(jobSummaryList)' --output text 2>/dev/null || echo "0")
RUNNABLE=$(aws batch list-jobs --job-queue ai-music-generator-queue --job-status RUNNABLE --region $AWS_REGION --profile $AWS_PROFILE --query 'length(jobSummaryList)' --output text 2>/dev/null || echo "0")
PENDING=$(aws batch list-jobs --job-queue ai-music-generator-queue --job-status PENDING --region $AWS_REGION --profile $AWS_PROFILE --query 'length(jobSummaryList)' --output text 2>/dev/null || echo "0")

if [ "$RUNNING" -gt 0 ]; then
  echo "   🟢 Running: $RUNNING"
fi
if [ "$RUNNABLE" -gt 0 ]; then
  echo "   🟡 Runnable: $RUNNABLE (waiting for GPU)"
fi
if [ "$PENDING" -gt 0 ]; then
  echo "   🟡 Pending: $PENDING"
fi
if [ "$RUNNING" -eq 0 ] && [ "$RUNNABLE" -eq 0 ] && [ "$PENDING" -eq 0 ]; then
  echo "   ✅ No active jobs"
fi
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                        Summary                             ║"
echo "╚════════════════════════════════════════════════════════════╝"

if [ "$GPU_QUOTA" == "0" ] || [ "$GPU_QUOTA" == "0.0" ]; then
  echo ""
  echo "⚠️  CRITICAL: GPU quota is 0"
  echo ""
  echo "   Next steps:"
  echo "   1. Request GPU quota increase:"
  echo "      https://console.aws.amazon.com/servicequotas/home/services/ec2/quotas/L-DB2E81BA"
  echo ""
  echo "   2. Wait for approval (24-48 hours)"
  echo ""
  echo "   3. Run this script again to verify"
  echo ""
else
  echo ""
  echo "✅ System is ready to process jobs!"
  echo ""
  echo "   Submit a job:"
  echo "   python aws_submit_job.py \\"
  echo "     --prompt \"your prompt\" \\"
  echo "     --duration 60 \\"
  echo "     --preset quality \\"
  echo "     --resolution 4k \\"
  echo "     --output-bucket $LATEST_BUCKET \\"
  echo "     --wait"
  echo ""
fi
