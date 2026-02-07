#!/bin/bash
# Build Docker image and push to AWS ECR

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Building and Pushing Docker Image${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install it first.${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install it first.${NC}"
    exit 1
fi

# Get AWS account ID and region
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=${AWS_REGION:-us-east-1}
REPOSITORY_NAME=${REPOSITORY_NAME:-ai-music-generator}

echo -e "${YELLOW}AWS Account ID:${NC} $AWS_ACCOUNT_ID"
echo -e "${YELLOW}AWS Region:${NC} $AWS_REGION"
echo -e "${YELLOW}Repository:${NC} $REPOSITORY_NAME"
echo ""

# ECR repository URL
ECR_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPOSITORY_NAME"

# Login to ECR
echo -e "${YELLOW}🔐 Logging in to ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build Docker image
echo ""
echo -e "${YELLOW}🏗️  Building Docker image...${NC}"
docker build -t $REPOSITORY_NAME:latest .

# Tag image
echo ""
echo -e "${YELLOW}🏷️  Tagging image...${NC}"
docker tag $REPOSITORY_NAME:latest $ECR_URL:latest
docker tag $REPOSITORY_NAME:latest $ECR_URL:$(date +%Y%m%d-%H%M%S)

# Push to ECR
echo ""
echo -e "${YELLOW}📤 Pushing to ECR...${NC}"
docker push $ECR_URL:latest
docker push $ECR_URL:$(date +%Y%m%d-%H%M%S)

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ Successfully pushed to ECR!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${YELLOW}Image URL:${NC} $ECR_URL:latest"
echo ""
