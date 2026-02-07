# 🏗️ Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                          │
│  (CI/CD, Terraform, Docker Build/Push, Job Submission)     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud                              │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   ECR        │───▶│  AWS Batch   │───▶│     S3       │ │
│  │  (Docker)    │    │  (GPU Jobs)  │    │  (Results)   │ │
│  └──────────────┘    └──────┬───────┘    └──────────────┘ │
│                             │                              │
│                             ▼                              │
│                    ┌─────────────────┐                     │
│                    │  AWS Bedrock    │                     │
│                    │  (SDXL/Titan)   │                     │
│                    └─────────────────┘                     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  VPC (10.0.0.0/16)                                   │  │
│  │  ├─ Subnet (10.0.1.0/24)                            │  │
│  │  ├─ Internet Gateway                                │  │
│  │  └─ Security Group                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Infrastructure

```
┌─────────────────────────────────────────────────────────────────────┐
│                          AWS Infrastructure                         │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  Region: us-east-1                                            │ │
│  │                                                               │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │  VPC (10.0.0.0/16)                                      │ │ │
│  │  │                                                         │ │ │
│  │  │  ┌───────────────────────────────────────────────────┐ │ │ │
│  │  │  │  Public Subnet (10.0.1.0/24)                      │ │ │ │
│  │  │  │                                                   │ │ │ │
│  │  │  │  ┌─────────────────────────────────────────────┐ │ │ │ │
│  │  │  │  │  AWS Batch Compute Environment          │ │ │ │ │
│  │  │  │  │                                             │ │ │ │ │
│  │  │  │  │  Type: MANAGED                              │ │ │ │ │
│  │  │  │  │  Instance: g4dn.xlarge (NVIDIA T4)          │ │ │ │ │
│  │  │  │  │  Pricing: SPOT (70% discount)               │ │ │ │ │
│  │  │  │  │  Min vCPUs: 0                               │ │ │ │ │
│  │  │  │  │  Max vCPUs: 16                              │ │ │ │ │
│  │  │  │  │  Auto-scaling: Enabled                      │ │ │ │ │
│  │  │  │  └─────────────────────────────────────────────┘ │ │ │ │
│  │  │  └───────────────────────────────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  ECR (Elastic Container Registry)                             │ │
│  │  - Repository: ai-music-generator                             │ │
│  │  - Image Scanning: Enabled                                    │ │
│  │  - Tags: latest, <commit-sha>                                 │ │
│  │  - Size: ~8GB (CUDA + Python + AI libs)                       │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  S3 Bucket                                                     │ │
│  │  - Name: ai-music-gen-{account-id}-{random}                   │ │
│  │  - Versioning: Enabled                                        │ │
│  │  - Structure:                                                 │ │
│  │    └─ output/                                                 │ │
│  │       └─ {job-id}/                                            │ │
│  │          ├─ music.wav                                         │ │
│  │          ├─ cover.png                                         │ │
│  │          ├─ video.mp4                                         │ │
│  │          └─ metadata.json                                     │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  AWS Bedrock                                                   │ │
│  │  - Model: stability.stable-diffusion-xl-v1                    │ │
│  │  - Model: amazon.titan-image-generator-v1                     │ │
│  │  - Region: us-east-1                                          │ │
│  │  - API: InvokeModel                                           │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  CloudWatch Logs                                               │ │
│  │  - Log Group: /aws/batch/ai-music-generator                   │ │
│  │  - Retention: 7 days                                          │ │
│  │  - Streams: Per job execution                                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  IAM Roles & Policies                                          │ │
│  │  ├─ batch-job-role (for containers)                           │ │
│  │  │  ├─ S3 access (read/write bucket)                          │ │
│  │  │  ├─ Bedrock access (invoke models)                         │ │
│  │  │  └─ ECR access (pull images)                               │ │
│  │  ├─ batch-service-role (for Batch)                            │ │
│  │  │  └─ AWSBatchServiceRole                                    │ │
│  │  └─ ecs-instance-role (for EC2)                               │ │
│  │     └─ AmazonEC2ContainerServiceforEC2Role                    │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Job Submission                              │
│  (GitHub Actions or CLI: aws_submit_job.py)                         │
└────────────┬────────────────────────────────────────────────────────┘
             │
             │ Submit job with parameters:
             │ - prompt: "cozy lofi coffee shop music"
             │ - duration: 60s
             │ - preset: balanced
             │ - resolution: 4k
             │ - bedrock_model: sdxl
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         AWS Batch Queue                             │
│  Job queued and waiting for available compute                       │
└────────────┬────────────────────────────────────────────────────────┘
             │
             │ Auto-scaling triggers
             │ EC2 instance launch (g4dn.xlarge Spot)
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Container Execution (GPU)                        │
│  Docker container from ECR with CUDA support                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  STEP 1: Music Generation (2-3 min)                         │  │
│  │  • Load MusicGen model (1.5GB)                              │  │
│  │  • Process prompt with GPU acceleration                     │  │
│  │  • Generate audio waveform (30-60s)                         │  │
│  │  • Save as WAV (high quality, 44.1kHz)                      │  │
│  │  • Output: /app/output/{job-id}/music.wav                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                            │                                        │
│                            ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  STEP 2: Image Generation (30-60s)                          │  │
│  │  • Enhance prompt for lofi/anime style                      │  │
│  │  • Call AWS Bedrock API (SDXL or Titan)                     │  │
│  │  • Generate image (3840x2160 for 4K)                        │  │
│  │  • Apply style: lofi, anime, studio ghibli                  │  │
│  │  • Save as PNG                                              │  │
│  │  • Output: /app/output/{job-id}/cover.png                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                            │                                        │
│                            ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  STEP 3: Video Composition (10-20s)                         │  │
│  │  • Load audio (music.wav)                                   │  │
│  │  • Load image (cover.png)                                   │  │
│  │  • FFmpeg processing:                                       │  │
│  │    - Video codec: libx264                                   │  │
│  │    - Audio codec: AAC (192k)                                │  │
│  │    - Pixel format: yuv420p                                  │  │
│  │    - Duration: match audio length                           │  │
│  │  • Save as MP4                                              │  │
│  │  • Output: /app/output/{job-id}/video.mp4                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                            │                                        │
│                            ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  STEP 4: Upload to S3 (5-10s)                               │  │
│  │  • Upload music.wav → S3                                    │  │
│  │  • Upload cover.png → S3                                    │  │
│  │  • Upload video.mp4 → S3                                    │  │
│  │  • Create metadata.json with job info                       │  │
│  │  • Upload metadata.json → S3                                │  │
│  │  • Location: s3://bucket/output/{job-id}/                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Total Time: 3-5 minutes                                           │
│  Total Cost: ~$0.06 per video                                      │
└────────────┬────────────────────────────────────────────────────────┘
             │
             │ Job completed
             │ Instance scales down to 0
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Results in S3                               │
│  s3://ai-music-gen-{account-id}-{random}/output/{job-id}/           │
│  ├─ music.wav (5-10 MB)                                             │
│  ├─ cover.png (2-5 MB for 4K)                                       │
│  ├─ video.mp4 (10-20 MB)                                            │
│  └─ metadata.json (1 KB)                                            │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

- **AWS Batch**: Managed compute for running AI workloads
- **EC2 (g4dn.xlarge)**: NVIDIA T4 GPU instances (Spot)
- **ECR**: Docker container registry
- **S3**: Object storage for outputs
- **Bedrock**: Managed AI models (SDXL, Titan)
- **VPC**: Isolated network environment
- **CloudWatch**: Logging and monitoring
- **IAM**: Security and permissions

## Technical Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Language** | Python | 3.10 | Main programming language |
| **Music AI** | MusicGen | Latest | Meta's music generation |
| **Image AI** | Bedrock SDXL | v1 | AWS managed Stable Diffusion |
| **Image AI** | Titan | v1 | AWS native image generation |
| **Video** | FFmpeg | Latest | Video composition |
| **Compute** | AWS Batch | - | Managed job scheduling |
| **GPU** | NVIDIA T4 | 16GB | Deep learning acceleration |
| **Container** | Docker | 20+ | Application packaging |
| **CUDA** | 11.8 | - | GPU computing platform |
| **IaC** | Terraform | 1.6+ | Infrastructure as code |
| **CI/CD** | GitHub Actions | - | Automation pipeline |
| **Storage** | S3 | - | Object storage |
| **Registry** | ECR | - | Container images |
| **Logs** | CloudWatch | - | Monitoring and debugging |
| **Network** | VPC | - | Isolated networking |

## Supported Regions

Currently deployed in:
- ✅ **us-east-1** (N. Virginia) - Primary region

Can be deployed in any AWS region with:
- AWS Batch support
- Bedrock availability
- g4dn instance availability

## Best Practices Implemented

- ✅ **Infrastructure as Code** - All resources defined in Terraform
- ✅ **Immutable Infrastructure** - Docker containers, no manual changes
- ✅ **Auto-scaling** - Scale to zero when idle
- ✅ **Cost Optimization** - Spot instances, efficient resource usage
- ✅ **Security** - IAM roles, VPC isolation, no hardcoded credentials
- ✅ **Monitoring** - CloudWatch logs for all jobs
- ✅ **CI/CD** - Automated testing and deployment
- ✅ **Documentation** - Comprehensive guides and examples
- ✅ **Version Control** - Git for all code and configuration
- ✅ **Modular Design** - Separate concerns, easy to extend
