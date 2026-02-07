#!/bin/bash
# Deploy infrastructure to AWS using Terraform

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Deploying to AWS${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}❌ Terraform not found. Please install it first.${NC}"
    echo -e "${YELLOW}💡 Install: https://www.terraform.io/downloads${NC}"
    exit 1
fi

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install it first.${NC}"
    exit 1
fi

# Check AWS credentials
echo -e "${YELLOW}🔐 Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured.${NC}"
    echo -e "${YELLOW}💡 Run: aws configure${NC}"
    exit 1
fi

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✅ AWS Account: $AWS_ACCOUNT_ID${NC}"
echo ""

# Navigate to terraform directory
cd terraform

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo -e "${YELLOW}⚠️  terraform.tfvars not found${NC}"
    echo -e "${YELLOW}💡 Creating from example...${NC}"
    cp terraform.tfvars.example terraform.tfvars
    echo ""
    echo -e "${RED}❌ Please edit terraform.tfvars with your configuration${NC}"
    echo -e "${YELLOW}   Especially set a unique S3 bucket name!${NC}"
    exit 1
fi

# Initialize Terraform
echo -e "${YELLOW}🔧 Initializing Terraform...${NC}"
terraform init

# Plan
echo ""
echo -e "${YELLOW}📋 Planning infrastructure...${NC}"
terraform plan -out=tfplan

# Ask for confirmation
echo ""
echo -e "${YELLOW}⚠️  Ready to deploy infrastructure to AWS${NC}"
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${RED}❌ Deployment cancelled${NC}"
    exit 1
fi

# Apply
echo ""
echo -e "${YELLOW}🚀 Deploying infrastructure...${NC}"
terraform apply tfplan

# Get outputs
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ Infrastructure deployed!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

ECR_URL=$(terraform output -raw ecr_repository_url)
S3_BUCKET=$(terraform output -raw s3_bucket_name)
JOB_QUEUE=$(terraform output -raw job_queue_name)
JOB_DEFINITION=$(terraform output -raw job_definition_name)

echo -e "${YELLOW}📦 ECR Repository:${NC} $ECR_URL"
echo -e "${YELLOW}🪣 S3 Bucket:${NC} $S3_BUCKET"
echo -e "${YELLOW}📋 Job Queue:${NC} $JOB_QUEUE"
echo -e "${YELLOW}⚙️  Job Definition:${NC} $JOB_DEFINITION"
echo ""

# Save outputs to file
cd ..
cat > aws_config.json <<EOF
{
  "ecr_repository_url": "$ECR_URL",
  "s3_bucket_name": "$S3_BUCKET",
  "job_queue_name": "$JOB_QUEUE",
  "job_definition_name": "$JOB_DEFINITION"
}
EOF

echo -e "${GREEN}✅ Configuration saved to aws_config.json${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Build and push Docker image: ${GREEN}./scripts/build_and_push.sh${NC}"
echo -e "  2. Submit a test job: ${GREEN}python aws_submit_job.py --prompt 'test' --output-bucket $S3_BUCKET${NC}"
echo ""
