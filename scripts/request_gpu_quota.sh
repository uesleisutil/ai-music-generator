#!/bin/bash
# Script to request GPU instance quota increase

AWS_PROFILE=${AWS_PROFILE:-b3tr}
AWS_REGION=${AWS_REGION:-us-east-1}

echo "📊 Checking current GPU instance quotas..."
echo ""

# Check On-Demand G instances quota
ONDEMAND_QUOTA=$(aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --region $AWS_REGION \
  --profile $AWS_PROFILE \
  --query 'Quota.Value' \
  --output text 2>/dev/null || echo "0")

echo "Current On-Demand G instances quota: $ONDEMAND_QUOTA vCPUs"
echo ""

if [ "$ONDEMAND_QUOTA" == "0" ] || [ "$ONDEMAND_QUOTA" == "0.0" ]; then
  echo "⚠️  Your account has 0 vCPUs quota for On-Demand G instances!"
  echo ""
  echo "📝 To request a quota increase:"
  echo ""
  echo "1. Go to AWS Service Quotas console:"
  echo "   https://console.aws.amazon.com/servicequotas/home/services/ec2/quotas/L-DB2E81BA"
  echo ""
  echo "2. Click 'Request quota increase'"
  echo ""
  echo "3. Request at least 4 vCPUs (for 1x g4dn.xlarge)"
  echo "   Recommended: 8 vCPUs (for flexibility)"
  echo ""
  echo "4. Provide justification:"
  echo "   'Need GPU instances for AI/ML workloads (music and video generation)'"
  echo ""
  echo "5. Wait for approval (usually 24-48 hours)"
  echo ""
  echo "💡 Alternative: Use Spot instances (usually have higher default quotas)"
  echo ""
else
  echo "✅ You have $ONDEMAND_QUOTA vCPUs quota for On-Demand G instances"
  echo ""
fi

# Check Spot G instances quota
SPOT_QUOTA=$(aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-3819A6DF \
  --region $AWS_REGION \
  --profile $AWS_PROFILE \
  --query 'Quota.Value' \
  --output text 2>/dev/null || echo "Unknown")

echo "Current Spot G instances quota: $SPOT_QUOTA vCPUs"
echo ""

if [ "$SPOT_QUOTA" != "0" ] && [ "$SPOT_QUOTA" != "0.0" ] && [ "$SPOT_QUOTA" != "Unknown" ]; then
  echo "✅ You can use Spot instances! Quota: $SPOT_QUOTA vCPUs"
  echo ""
  echo "💡 Recommendation: Switch back to Spot instances for now"
  echo "   Spot instances are cheaper and you have quota available"
  echo ""
fi
