#!/bin/bash
# Script to warm up GPU instance before submitting jobs
# This keeps the instance running for approximately 1 hour

set -e

AWS_PROFILE=${AWS_PROFILE:-b3tr}
AWS_REGION=${AWS_REGION:-us-east-1}
COMPUTE_ENV="ai-music-generator-gpu-spot"
DURATION_MINUTES=${1:-60}  # Default 60 minutes

echo "🔥 Warming up GPU instance..."
echo "   Compute Environment: $COMPUTE_ENV"
echo "   Duration: $DURATION_MINUTES minutes"
echo "   Profile: $AWS_PROFILE"
echo ""

# Update compute environment to keep 1 instance (4 vCPUs = g4dn.xlarge)
echo "⏳ Requesting GPU instance..."
aws batch update-compute-environment \
  --compute-environment $COMPUTE_ENV \
  --compute-resources desiredVcpus=4 \
  --region $AWS_REGION \
  --profile $AWS_PROFILE

echo "✅ GPU instance requested (will provision in 3-5 minutes)"
echo ""
echo "💡 The instance will stay warm for approximately $DURATION_MINUTES minutes"
echo "   After that, it will scale down to 0 when no jobs are running"
echo ""
echo "📝 To submit a job now:"
echo "   python aws_submit_job.py --prompt \"your prompt\" --duration 60 --preset quality --resolution 4k --output-bucket <bucket-name> --wait"
echo ""

# Optional: Schedule scale down after duration
if command -v at &> /dev/null; then
  echo "⏰ Scheduling automatic scale down in $DURATION_MINUTES minutes..."
  
  # Create a script to scale down
  cat > /tmp/scale_down_gpu.sh << EOF
#!/bin/bash
aws batch update-compute-environment \
  --compute-environment $COMPUTE_ENV \
  --compute-resources desiredVcpus=0 \
  --region $AWS_REGION \
  --profile $AWS_PROFILE
echo "✅ GPU instance scaled down to 0"
EOF
  
  chmod +x /tmp/scale_down_gpu.sh
  echo "/tmp/scale_down_gpu.sh" | at now + $DURATION_MINUTES minutes 2>/dev/null || true
  echo "✅ Scheduled scale down"
else
  echo "⚠️  'at' command not available - automatic scale down not scheduled"
  echo "   The instance will scale down automatically when no jobs are running"
fi

echo ""
echo "🎵 Ready to process jobs!"
