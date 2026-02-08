#!/bin/bash
# Script to clean up old S3 buckets from failed deployments

set -e

AWS_PROFILE=${AWS_PROFILE:-b3tr}
AWS_REGION=${AWS_REGION:-us-east-1}
PROJECT_PREFIX="ai-music-gen"

echo "🧹 Cleaning up old S3 buckets..."
echo "   Project: $PROJECT_PREFIX"
echo "   Region: $AWS_REGION"
echo "   Profile: $AWS_PROFILE"
echo ""

# Get all buckets with project prefix, sorted by creation date
BUCKETS=$(aws s3api list-buckets \
  --profile $AWS_PROFILE \
  --query "Buckets[?starts_with(Name, '$PROJECT_PREFIX')].{Name:Name,Date:CreationDate}" \
  --output text | sort -k2 -r)

if [ -z "$BUCKETS" ]; then
  echo "✅ No buckets found to clean up"
  exit 0
fi

# Count total buckets
TOTAL=$(echo "$BUCKETS" | wc -l | xargs)
echo "Found $TOTAL bucket(s)"
echo ""

# Get the most recent bucket (first line)
LATEST_BUCKET=$(echo "$BUCKETS" | head -1 | awk '{print $1}')
echo "📌 Keeping latest bucket: $LATEST_BUCKET"
echo ""

# Get old buckets (all except first)
OLD_BUCKETS=$(echo "$BUCKETS" | tail -n +2 | awk '{print $1}')

if [ -z "$OLD_BUCKETS" ]; then
  echo "✅ No old buckets to delete"
  exit 0
fi

echo "🗑️  Deleting old buckets:"
for bucket in $OLD_BUCKETS; do
  echo "   - $bucket"
done
echo ""

read -p "⚠️  Are you sure you want to delete these buckets? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  echo "❌ Cancelled"
  exit 0
fi

echo ""

for bucket in $OLD_BUCKETS; do
  echo "🗑️  Deleting bucket: $bucket"
  
  # Check if bucket has versioning enabled
  VERSIONING=$(aws s3api get-bucket-versioning \
    --bucket $bucket \
    --profile $AWS_PROFILE \
    --query 'Status' \
    --output text 2>/dev/null || echo "None")
  
  if [ "$VERSIONING" == "Enabled" ]; then
    echo "   Removing all versions..."
    aws s3api delete-objects \
      --bucket $bucket \
      --profile $AWS_PROFILE \
      --delete "$(aws s3api list-object-versions \
        --bucket $bucket \
        --profile $AWS_PROFILE \
        --query '{Objects: Versions[].{Key:Key,VersionId:VersionId}}' \
        --max-items 1000)" 2>/dev/null || true
    
    # Delete delete markers
    aws s3api delete-objects \
      --bucket $bucket \
      --profile $AWS_PROFILE \
      --delete "$(aws s3api list-object-versions \
        --bucket $bucket \
        --profile $AWS_PROFILE \
        --query '{Objects: DeleteMarkers[].{Key:Key,VersionId:VersionId}}' \
        --max-items 1000)" 2>/dev/null || true
  fi
  
  # Empty bucket
  echo "   Emptying bucket..."
  aws s3 rm s3://$bucket --recursive --profile $AWS_PROFILE 2>/dev/null || true
  
  # Delete bucket
  echo "   Deleting bucket..."
  aws s3api delete-bucket --bucket $bucket --profile $AWS_PROFILE 2>/dev/null || true
  
  echo "   ✅ Deleted"
  echo ""
done

echo "✅ Cleanup complete!"
echo ""
echo "📌 Active bucket: $LATEST_BUCKET"
