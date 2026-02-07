#!/bin/bash
# Script to clean up orphaned VPCs from failed deployments

set -e

AWS_PROFILE=${AWS_PROFILE:-b3tr}
AWS_REGION=${AWS_REGION:-us-east-1}
PROJECT_NAME="ai-music-generator"

echo "🧹 Cleaning up orphaned VPCs..."
echo "   Project: $PROJECT_NAME"
echo "   Region: $AWS_REGION"
echo "   Profile: $AWS_PROFILE"
echo ""

# Get all VPCs for this project
VPC_IDS=$(aws ec2 describe-vpcs \
  --region $AWS_REGION \
  --profile $AWS_PROFILE \
  --filters "Name=tag:Project,Values=$PROJECT_NAME" \
  --query 'Vpcs[].VpcId' \
  --output text)

if [ -z "$VPC_IDS" ]; then
  echo "✅ No VPCs found to clean up"
  exit 0
fi

echo "Found VPCs to delete:"
for vpc_id in $VPC_IDS; do
  echo "  - $vpc_id"
done
echo ""

for vpc_id in $VPC_IDS; do
  echo "🗑️  Deleting VPC: $vpc_id"
  
  # Delete NAT Gateways
  echo "   Deleting NAT Gateways..."
  NAT_GWS=$(aws ec2 describe-nat-gateways \
    --region $AWS_REGION \
    --profile $AWS_PROFILE \
    --filter "Name=vpc-id,Values=$vpc_id" \
    --query 'NatGateways[?State!=`deleted`].NatGatewayId' \
    --output text)
  
  for nat_gw in $NAT_GWS; do
    echo "     Deleting NAT Gateway: $nat_gw"
    aws ec2 delete-nat-gateway --nat-gateway-id $nat_gw --region $AWS_REGION --profile $AWS_PROFILE || true
  done
  
  # Wait a bit for NAT gateways to start deleting
  if [ ! -z "$NAT_GWS" ]; then
    echo "     Waiting for NAT Gateways to delete..."
    sleep 10
  fi
  
  # Delete Internet Gateways
  echo "   Deleting Internet Gateways..."
  IGW_IDS=$(aws ec2 describe-internet-gateways \
    --region $AWS_REGION \
    --profile $AWS_PROFILE \
    --filters "Name=attachment.vpc-id,Values=$vpc_id" \
    --query 'InternetGateways[].InternetGatewayId' \
    --output text)
  
  for igw_id in $IGW_IDS; do
    echo "     Detaching IGW: $igw_id"
    aws ec2 detach-internet-gateway --internet-gateway-id $igw_id --vpc-id $vpc_id --region $AWS_REGION --profile $AWS_PROFILE || true
    echo "     Deleting IGW: $igw_id"
    aws ec2 delete-internet-gateway --internet-gateway-id $igw_id --region $AWS_REGION --profile $AWS_PROFILE || true
  done
  
  # Delete Subnets
  echo "   Deleting Subnets..."
  SUBNET_IDS=$(aws ec2 describe-subnets \
    --region $AWS_REGION \
    --profile $AWS_PROFILE \
    --filters "Name=vpc-id,Values=$vpc_id" \
    --query 'Subnets[].SubnetId' \
    --output text)
  
  for subnet_id in $SUBNET_IDS; do
    echo "     Deleting Subnet: $subnet_id"
    aws ec2 delete-subnet --subnet-id $subnet_id --region $AWS_REGION --profile $AWS_PROFILE || true
  done
  
  # Delete Route Tables (except main)
  echo "   Deleting Route Tables..."
  RT_IDS=$(aws ec2 describe-route-tables \
    --region $AWS_REGION \
    --profile $AWS_PROFILE \
    --filters "Name=vpc-id,Values=$vpc_id" \
    --query 'RouteTables[?Associations[0].Main!=`true`].RouteTableId' \
    --output text)
  
  for rt_id in $RT_IDS; do
    echo "     Deleting Route Table: $rt_id"
    aws ec2 delete-route-table --route-table-id $rt_id --region $AWS_REGION --profile $AWS_PROFILE || true
  done
  
  # Delete Security Groups (except default)
  echo "   Deleting Security Groups..."
  SG_IDS=$(aws ec2 describe-security-groups \
    --region $AWS_REGION \
    --profile $AWS_PROFILE \
    --filters "Name=vpc-id,Values=$vpc_id" \
    --query 'SecurityGroups[?GroupName!=`default`].GroupId' \
    --output text)
  
  for sg_id in $SG_IDS; do
    echo "     Deleting Security Group: $sg_id"
    aws ec2 delete-security-group --group-id $sg_id --region $AWS_REGION --profile $AWS_PROFILE || true
  done
  
  # Delete VPC
  echo "   Deleting VPC: $vpc_id"
  aws ec2 delete-vpc --vpc-id $vpc_id --region $AWS_REGION --profile $AWS_PROFILE || true
  
  echo "   ✅ VPC $vpc_id deleted"
  echo ""
done

echo "✅ Cleanup complete!"
