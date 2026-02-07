# AI Music Generator - AWS Infrastructure
# This Terraform configuration sets up AWS Batch with GPU instances

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource tagging"
  type        = string
  default     = "ai-music-generator"
}

variable "s3_bucket_name" {
  description = "S3 bucket for outputs (leave empty for auto-generated)"
  type        = string
  default     = ""
}

# Auto-generate unique bucket name if not provided
locals {
  # Get AWS account ID
  account_id = data.aws_caller_identity.current.account_id
  
  # Generate unique bucket name: ai-music-gen-{account_id}-{random}
  bucket_name = var.s3_bucket_name != "" ? var.s3_bucket_name : "ai-music-gen-${local.account_id}-${random_id.bucket_suffix.hex}"
}

# Random suffix for bucket name
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Get current AWS account info
data "aws_caller_identity" "current" {}

variable "ecr_repository_name" {
  description = "ECR repository name"
  type        = string
  default     = "ai-music-generator"
}

# S3 Bucket for outputs
resource "aws_s3_bucket" "output_bucket" {
  bucket = local.bucket_name
  
  tags = {
    Name    = "${var.project_name}-output"
    Project = var.project_name
  }
}

resource "aws_s3_bucket_versioning" "output_bucket" {
  bucket = aws_s3_bucket.output_bucket.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Use existing ECR Repository (created by GitHub Actions)
# If it doesn't exist, the workflow will create it before Terraform runs
data "aws_ecr_repository" "app" {
  name = var.ecr_repository_name
}

# IAM Role for Batch Jobs
resource "aws_iam_role" "batch_job_role" {
  name = "${var.project_name}-batch-job-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Name    = "${var.project_name}-batch-job-role"
    Project = var.project_name
  }
}

# IAM Policy for S3 access
resource "aws_iam_role_policy" "batch_job_s3_policy" {
  name = "${var.project_name}-s3-policy"
  role = aws_iam_role.batch_job_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.output_bucket.arn,
          "${aws_s3_bucket.output_bucket.arn}/*"
        ]
      }
    ]
  })
}

# IAM Policy for Bedrock access
resource "aws_iam_role_policy" "batch_job_bedrock_policy" {
  name = "${var.project_name}-bedrock-policy"
  role = aws_iam_role.batch_job_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = [
          "arn:aws:bedrock:*::foundation-model/stability.stable-diffusion-xl-v1",
          "arn:aws:bedrock:*::foundation-model/amazon.titan-image-generator-v1"
        ]
      }
    ]
  })
}

# IAM Policy for ECR access
resource "aws_iam_role_policy_attachment" "batch_job_ecr_policy" {
  role       = aws_iam_role.batch_job_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# IAM Role for Batch Service
resource "aws_iam_role" "batch_service_role" {
  name = "${var.project_name}-batch-service-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "batch.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Name    = "${var.project_name}-batch-service-role"
    Project = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "batch_service_policy" {
  role       = aws_iam_role.batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

# IAM Role for EC2 instances
resource "aws_iam_role" "ecs_instance_role" {
  name = "${var.project_name}-ecs-instance-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Name    = "${var.project_name}-ecs-instance-role"
    Project = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "ecs_instance_policy" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "${var.project_name}-ecs-instance-profile"
  role = aws_iam_role.ecs_instance_role.name
}

# Security Group
resource "aws_security_group" "batch_sg" {
  name        = "${var.project_name}-batch-sg"
  description = "Security group for Batch compute environment"
  vpc_id      = aws_vpc.batch_vpc.id
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name    = "${var.project_name}-batch-sg"
    Project = var.project_name
  }
}

# Launch Template for GPU instances
resource "aws_launch_template" "batch_lt" {
  name_prefix = "${var.project_name}-batch-"
  
  block_device_mappings {
    device_name = "/dev/xvda"
    
    ebs {
      volume_size           = 100
      volume_type           = "gp3"
      delete_on_termination = true
    }
  }
  
  tag_specifications {
    resource_type = "instance"
    
    tags = {
      Name    = "${var.project_name}-batch-instance"
      Project = var.project_name
    }
  }
}

# Batch Compute Environment (Spot instances for cost savings)
resource "aws_batch_compute_environment" "gpu_spot" {
  compute_environment_name = "${var.project_name}-gpu-spot"
  type                     = "MANAGED"
  service_role             = aws_iam_role.batch_service_role.arn
  
  compute_resources {
    type                = "SPOT"
    allocation_strategy = "SPOT_CAPACITY_OPTIMIZED"
    bid_percentage      = 100
    
    instance_role = aws_iam_instance_profile.ecs_instance_profile.arn
    instance_type = [
      "g4dn.xlarge",
      "g4dn.2xlarge"
    ]
    
    min_vcpus     = 0  # Scale down to 0 when no jobs (saves cost)
    max_vcpus     = 16
    desired_vcpus = 0  # Start with no instances
    
    security_group_ids = [aws_security_group.batch_sg.id]
    
    subnets = [aws_subnet.batch_subnet.id]
    
    launch_template {
      launch_template_id = aws_launch_template.batch_lt.id
      version            = "$Latest"
    }
    
    tags = {
      Name    = "${var.project_name}-batch-compute"
      Project = var.project_name
    }
  }
  
  depends_on = [aws_iam_role_policy_attachment.batch_service_policy]
}

# Create VPC for AWS Batch
resource "aws_vpc" "batch_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name    = "${var.project_name}-vpc"
    Project = var.project_name
  }
}

# Internet Gateway
resource "aws_internet_gateway" "batch_igw" {
  vpc_id = aws_vpc.batch_vpc.id
  
  tags = {
    Name    = "${var.project_name}-igw"
    Project = var.project_name
  }
}

# Public Subnet
resource "aws_subnet" "batch_subnet" {
  vpc_id                  = aws_vpc.batch_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[0]
  
  tags = {
    Name    = "${var.project_name}-subnet"
    Project = var.project_name
  }
}

# Route Table
resource "aws_route_table" "batch_rt" {
  vpc_id = aws_vpc.batch_vpc.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.batch_igw.id
  }
  
  tags = {
    Name    = "${var.project_name}-rt"
    Project = var.project_name
  }
}

# Route Table Association
resource "aws_route_table_association" "batch_rta" {
  subnet_id      = aws_subnet.batch_subnet.id
  route_table_id = aws_route_table.batch_rt.id
}

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
}

# Batch Job Queue
resource "aws_batch_job_queue" "gpu_queue" {
  name     = "${var.project_name}-queue"
  state    = "ENABLED"
  priority = 1
  
  compute_environment_order {
    order               = 1
    compute_environment = aws_batch_compute_environment.gpu_spot.arn
  }
  
  tags = {
    Name    = "${var.project_name}-queue"
    Project = var.project_name
  }
}

# Batch Job Definition
resource "aws_batch_job_definition" "gpu_job" {
  name = "${var.project_name}-job"
  type = "container"
  
  platform_capabilities = ["EC2"]
  
  container_properties = jsonencode({
    image = "${data.aws_ecr_repository.app.repository_url}:latest"
    
    resourceRequirements = [
      {
        type  = "VCPU"
        value = "4"
      },
      {
        type  = "MEMORY"
        value = "15360"
      },
      {
        type  = "GPU"
        value = "1"
      }
    ]
    
    jobRoleArn = aws_iam_role.batch_job_role.arn
    
    environment = [
      {
        name  = "AWS_DEFAULT_REGION"
        value = var.aws_region
      }
    ]
    
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/aws/batch/${var.project_name}"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "job"
      }
    }
  })
  
  tags = {
    Name    = "${var.project_name}-job"
    Project = var.project_name
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "batch_logs" {
  name              = "/aws/batch/${var.project_name}"
  retention_in_days = 7
  
  tags = {
    Name    = "${var.project_name}-logs"
    Project = var.project_name
  }
}

# Outputs
output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = data.aws_ecr_repository.app.repository_url
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.output_bucket.id
}

output "job_queue_name" {
  description = "Batch job queue name"
  value       = aws_batch_job_queue.gpu_queue.name
}

output "job_definition_name" {
  description = "Batch job definition name"
  value       = aws_batch_job_definition.gpu_job.name
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group"
  value       = aws_cloudwatch_log_group.batch_logs.name
}
