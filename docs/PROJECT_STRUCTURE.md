# 📦 Project Structure

Complete file tree and component descriptions for the AI Music Generator.

---

## Directory Tree

```
ai-music-generator/
├── .github/
│   ├── workflows/
│   │   ├── deploy-aws.yml          # Main deployment pipeline
│   │   ├── test-deployment.yml     # Test job submission
│   │   ├── destroy-infrastructure.yml  # Cleanup workflow
│   │   └── validate.yml            # PR validation
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── FUNDING.yml
│   └── pull_request_template.md
│
├── docs/
│   ├── AI_SETUP.md                 # AI models configuration
│   ├── ARCHITECTURE.md             # Infrastructure diagrams
│   ├── AWS_PRICING.md              # Detailed cost breakdown
│   ├── AWS_SETUP.md                # Manual AWS setup
│   ├── CODE_OF_CONDUCT.md          # Community guidelines
│   ├── CONTRIBUTING.md             # Contribution guide
│   ├── MODELS.md                   # Complete model reference
│   └── PROJECT_STRUCTURE.md        # This file
│
├── examples/
│   └── batch_generate.py           # Batch job submission example
│
├── scripts/
│   ├── build_and_push.sh           # Docker build and ECR push
│   └── deploy_aws.sh               # Manual Terraform deployment
│
├── src/
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── generate_music_ai.py    # MusicGen, AudioLDM, Riffusion
│   │   ├── generate_image_ai.py    # Local Stable Diffusion models
│   │   └── generate_image_bedrock.py  # AWS Bedrock (SDXL, Titan)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── create_video.py         # FFmpeg video composition
│   │   └── upload_youtube.py       # YouTube API integration
│   ├── __init__.py
│   └── pipeline_ai.py              # Main orchestration pipeline
│
├── terraform/
│   └── main.tf                     # Complete infrastructure as code
│
├── .dockerignore
├── .gitignore
├── aws_batch_worker.py             # Container entrypoint for jobs
├── aws_submit_job.py               # CLI for job submission
├── Dockerfile                      # CUDA-enabled container
├── LICENSE                         # MIT License
├── models_config.yaml              # AI models configuration
├── QUICK_SETUP.md                  # 5-minute setup guide
├── README.md                       # Main documentation
├── requirements.txt                # Basic Python dependencies
├── requirements-aws.txt            # AWS SDK (boto3)
└── requirements-full.txt           # All AI dependencies
```

---

## Core Components

### 🚀 Entry Points

#### `aws_batch_worker.py` (~200 lines)
Container entrypoint that runs inside AWS Batch jobs.

**Responsibilities**:
- Parse job parameters from environment variables
- Execute the AI pipeline
- Upload results to S3
- Handle errors and logging

**Key Functions**:
- `main()` - Entry point
- `parse_job_params()` - Extract parameters
- `run_pipeline()` - Execute generation
- `upload_to_s3()` - Store results

#### `aws_submit_job.py` (~150 lines)
CLI tool for submitting jobs to AWS Batch.

**Responsibilities**:
- Parse command-line arguments
- Submit jobs to AWS Batch queue
- Wait for job completion (optional)
- Display job status

**Usage**:
```bash
python aws_submit_job.py \
  --prompt "lofi music" \
  --duration 60 \
  --preset balanced \
  --resolution 4k \
  --wait
```

---

## 🎵 Source Code (`src/`)

### Main Pipeline

#### `src/pipeline_ai.py` (~200 lines)
Orchestrates the complete generation pipeline.

**Responsibilities**:
- Coordinate music, image, and video generation
- Handle different presets and configurations
- Manage temporary files
- Error handling and retries

**Key Functions**:
- `generate_music_video()` - Main pipeline
- `select_models()` - Choose models based on preset
- `cleanup_temp_files()` - Resource management

**Flow**:
1. Generate music (2-3 min)
2. Generate image (30-60s)
3. Create video (10-20s)
4. Return file paths

### Generators

#### `src/generators/generate_music_ai.py` (~250 lines)
Music generation using multiple AI models.

**Supported Models**:
- MusicGen (small, medium, large, melody)
- AudioLDM (base, large)
- Riffusion

**Key Functions**:
- `generate_music()` - Main entry point
- `load_model()` - Model initialization
- `process_audio()` - Post-processing
- `save_wav()` - Export audio

**Parameters**:
- `prompt` - Text description
- `duration` - Length in seconds
- `model` - Model name
- `temperature` - Creativity (0.0-1.0)
- `top_k` - Sampling parameter

#### `src/generators/generate_image_bedrock.py` (~200 lines)
Image generation using AWS Bedrock.

**Supported Models**:
- Stable Diffusion XL (sdxl)
- Amazon Titan (titan)

**Key Functions**:
- `generate_image()` - Main entry point
- `enhance_prompt()` - Add lofi/anime style
- `call_bedrock_api()` - AWS API interaction
- `decode_image()` - Base64 to PNG

**Prompt Enhancement**:
- Adds lofi aesthetic keywords
- Includes anime/studio ghibli style
- Optimizes for cover art

**Parameters**:
- `prompt` - Base description
- `model` - sdxl or titan
- `resolution` - Output size
- `style` - lofi, anime, realistic

#### `src/generators/generate_image_ai.py` (~300 lines)
Local image generation (alternative to Bedrock).

**Supported Models**:
- Stable Diffusion 2.1
- Stable Diffusion XL Base
- Kandinsky 2.2
- Wuerstchen
- DeepFloyd IF
- ControlNet

**Note**: Requires GPU and large model downloads. Bedrock is recommended for production.

### Utilities

#### `src/utils/create_video.py` (~150 lines)
Video composition using FFmpeg.

**Responsibilities**:
- Combine audio and image
- Handle multiple resolutions
- Optimize for YouTube
- Add metadata

**Key Functions**:
- `create_video()` - Main composition
- `get_resolution()` - Parse resolution string
- `run_ffmpeg()` - Execute FFmpeg command

**Supported Resolutions**:
- HD (720p): 1280x720
- FHD (1080p): 1920x1080
- 2K (1440p): 2560x1440
- 4K (2160p): 3840x2160
- YouTube: 1920x1080 (optimized)

**FFmpeg Settings**:
- Video codec: libx264
- Audio codec: AAC (192k)
- Pixel format: yuv420p
- Preset: medium
- CRF: 23 (quality)

#### `src/utils/upload_youtube.py` (~200 lines)
YouTube API integration (in progress).

**Planned Features**:
- OAuth authentication
- Video upload
- Metadata management
- Playlist creation

---

## 🏗️ Infrastructure (`terraform/`)

### `terraform/main.tf` (~400 lines)
Complete AWS infrastructure definition.

**Resources Created**:

#### Networking
- VPC (10.0.0.0/16)
- Public subnet (10.0.1.0/24)
- Internet gateway
- Route table
- Security group

#### Compute
- AWS Batch compute environment
- Job queue
- Job definition
- Launch template

#### Storage
- S3 bucket (auto-generated name)
- Bucket versioning
- Lifecycle policies

#### Container Registry
- ECR repository
- Image scanning
- Lifecycle policies

#### IAM
- Batch service role
- ECS instance role
- Job execution role
- Policies for S3, Bedrock, ECR

#### Monitoring
- CloudWatch log group
- Log retention (7 days)

**Outputs**:
- `s3_bucket_name` - Results storage
- `ecr_repository_url` - Docker images
- `job_definition_name` - Batch job
- `cloudwatch_log_group` - Logs

**Variables**:
- `aws_region` - Deployment region
- `project_name` - Resource prefix
- `max_vcpus` - Scaling limit
- `spot_bid_percentage` - Cost savings

---

## 🐳 Container (`Dockerfile`)

### Multi-stage Build (~50 lines)

**Base Image**: `nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04`

**Installed Components**:
1. System packages (Python, FFmpeg, pkg-config)
2. Python dependencies (PyTorch, Transformers, etc.)
3. Application code
4. Model configuration

**Layers**:
- CUDA runtime (2GB)
- Python packages (4GB)
- Application code (50MB)
- Total size: ~8GB

**Optimizations**:
- Multi-stage build
- Layer caching
- Minimal base image
- No dev dependencies

---

## ⚙️ Configuration Files

### `models_config.yaml` (~150 lines)
AI models configuration.

**Structure**:
```yaml
music_models:
  musicgen-small:
    model_id: facebook/musicgen-small
    size: 300MB
    gpu_required: false
  # ... 6 more models

image_models:
  sdxl:
    provider: bedrock
    model_id: stability.stable-diffusion-xl-v1
    cost_per_image: 0.04
  # ... 8 more models

presets:
  balanced:
    music_model: musicgen-medium
    image_model: sdxl
    duration: 60
  # ... 3 more presets
```

### `requirements.txt` (~10 lines)
Basic Python dependencies for local development.

### `requirements-aws.txt` (~5 lines)
AWS SDK for job submission.

**Packages**:
- boto3 (AWS SDK)
- botocore (AWS core)

### `requirements-full.txt` (~30 lines)
Complete AI dependencies for container.

**Key Packages**:
- torch (PyTorch with CUDA)
- transformers (Hugging Face)
- diffusers (Stable Diffusion)
- audiocraft (MusicGen)
- accelerate (GPU optimization)
- av (video processing)
- boto3 (AWS SDK)

---

## 🔄 CI/CD (`.github/workflows/`)

### `deploy-aws.yml` (~150 lines)
Main deployment pipeline.

**Triggers**: Push to main branch

**Steps**:
1. Checkout code
2. Configure AWS credentials
3. Terraform init
4. Terraform plan
5. Terraform apply
6. Docker build (with CUDA)
7. Docker push to ECR
8. Update job definition

**Secrets Required**:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### `test-deployment.yml` (~100 lines)
Job submission and testing.

**Triggers**: Manual (workflow_dispatch)

**Inputs**:
- `prompt` - Music description
- `duration` - Length in seconds
- `preset` - quick/balanced/quality
- `resolution` - hd/fhd/2k/4k
- `bedrock_model` - sdxl/titan

**Steps**:
1. Get S3 bucket name
2. Submit job to AWS Batch
3. Wait for completion
4. Download results
5. Upload as artifact

### `destroy-infrastructure.yml` (~50 lines)
Infrastructure cleanup.

**Triggers**: Manual (requires "destroy" confirmation)

**Steps**:
1. Empty S3 bucket
2. Delete ECR images
3. Terraform destroy

### `validate.yml` (~80 lines)
PR validation.

**Triggers**: Pull requests

**Checks**:
- Python syntax
- Terraform format
- Terraform validate
- Dockerfile lint

---

## 📜 Scripts

### `scripts/build_and_push.sh` (~50 lines)
Docker build and ECR push automation.

**Usage**:
```bash
./scripts/build_and_push.sh
```

**Steps**:
1. Get AWS account ID
2. Login to ECR
3. Build Docker image
4. Tag image
5. Push to ECR

### `scripts/deploy_aws.sh` (~80 lines)
Manual Terraform deployment.

**Usage**:
```bash
./scripts/deploy_aws.sh
```

**Steps**:
1. Check AWS credentials
2. Terraform init
3. Terraform plan
4. Terraform apply
5. Build and push Docker
6. Display outputs

---

## 📖 Examples

### `examples/batch_generate.py` (~100 lines)
Batch job submission example.

**Features**:
- Submit multiple jobs
- Different prompts and settings
- Progress tracking
- Result download

**Usage**:
```bash
python examples/batch_generate.py
```

**Example Prompts**:
- Lofi coffee shop music
- Peaceful forest ambience
- Upbeat electronic music
- Relaxing piano melody

---

## 📚 Documentation (`docs/`)

### `docs/ARCHITECTURE.md`
Detailed infrastructure diagrams and explanations.

**Contents**:
- System architecture
- Network topology
- Data flow
- Component interactions
- Security model

### `docs/AWS_SETUP.md`
Manual AWS configuration guide.

**Contents**:
- IAM user creation
- Policy attachments
- Bedrock model access
- Region selection
- Troubleshooting

### `docs/AWS_PRICING.md`
Detailed cost breakdown.

**Contents**:
- Per-component costs
- Monthly estimates
- Cost optimization tips
- Spot vs On-Demand comparison

### `docs/AI_SETUP.md`
AI models configuration guide.

**Contents**:
- Model selection
- GPU requirements
- Quality comparisons
- Performance benchmarks

### `docs/MODELS.md`
Complete model reference.

**Contents**:
- All 13 AI models
- Parameters and options
- Use cases
- Examples

### `docs/CONTRIBUTING.md`
Contribution guidelines.

**Contents**:
- Code style
- PR process
- Testing requirements
- Documentation standards

### `docs/CODE_OF_CONDUCT.md`
Community guidelines.

**Contents**:
- Expected behavior
- Unacceptable behavior
- Enforcement
- Contact information

---

## 🔑 Key Files Summary

| File | Lines | Purpose | Complexity |
|------|-------|---------|------------|
| `terraform/main.tf` | ~400 | Infrastructure | High |
| `src/generators/generate_image_ai.py` | ~300 | Local image gen | High |
| `src/generators/generate_music_ai.py` | ~250 | Music generation | High |
| `src/pipeline_ai.py` | ~200 | Orchestration | Medium |
| `aws_batch_worker.py` | ~200 | Job worker | Medium |
| `src/generators/generate_image_bedrock.py` | ~200 | Bedrock images | Medium |
| `src/utils/upload_youtube.py` | ~200 | YouTube upload | Medium |
| `src/utils/create_video.py` | ~150 | Video composition | Medium |
| `aws_submit_job.py` | ~150 | Job submission | Low |
| `models_config.yaml` | ~150 | Configuration | Low |
| `.github/workflows/deploy-aws.yml` | ~150 | CI/CD | Medium |
| `.github/workflows/test-deployment.yml` | ~100 | Testing | Low |
| `examples/batch_generate.py` | ~100 | Examples | Low |
| `.github/workflows/validate.yml` | ~80 | Validation | Low |
| `scripts/deploy_aws.sh` | ~80 | Deployment | Low |
| `Dockerfile` | ~50 | Container | Low |
| `scripts/build_and_push.sh` | ~50 | Build script | Low |
| `.github/workflows/destroy-infrastructure.yml` | ~50 | Cleanup | Low |

**Total**: ~3,000 lines of code

---

## 🎯 Component Dependencies

```
aws_submit_job.py
    └─> AWS Batch API
        └─> aws_batch_worker.py (in container)
            └─> src/pipeline_ai.py
                ├─> src/generators/generate_music_ai.py
                │   └─> MusicGen models
                ├─> src/generators/generate_image_bedrock.py
                │   └─> AWS Bedrock API
                └─> src/utils/create_video.py
                    └─> FFmpeg
```

---

## 🔄 Data Flow

```
1. User submits job
   ↓
2. Job queued in AWS Batch
   ↓
3. EC2 instance launches (g4dn.xlarge)
   ↓
4. Container starts from ECR
   ↓
5. aws_batch_worker.py executes
   ↓
6. pipeline_ai.py orchestrates:
   ├─> generate_music_ai.py → music.wav
   ├─> generate_image_bedrock.py → cover.png
   └─> create_video.py → video.mp4
   ↓
7. Results uploaded to S3
   ↓
8. Container exits
   ↓
9. Instance scales down
```

---

## 📦 File Sizes

| Component | Size | Notes |
|-----------|------|-------|
| Docker image | ~8GB | CUDA + Python + AI libs |
| MusicGen medium | ~1.5GB | Downloaded on first run |
| Generated music | 5-10MB | WAV format, 44.1kHz |
| Generated image (4K) | 2-5MB | PNG format |
| Generated video | 10-20MB | MP4, H.264 codec |
| Terraform state | ~50KB | Infrastructure state |
| CloudWatch logs | ~1MB/job | Execution logs |

---

## 🔐 Security

### Secrets Management
- AWS credentials in GitHub Secrets
- No hardcoded credentials
- IAM roles for container access

### Network Security
- VPC isolation
- Security groups
- No public IPs on containers

### Data Security
- S3 encryption at rest
- HTTPS for all API calls
- Temporary file cleanup

---

## 🚀 Performance

### Optimization Strategies
- GPU acceleration (3-5x faster)
- Spot instances (70% cost savings)
- Auto-scaling (0 to 16 vCPUs)
- Docker layer caching
- Model caching in container

### Bottlenecks
- Music generation: 2-3 min (GPU-bound)
- Image generation: 30-60s (API latency)
- Video composition: 10-20s (CPU-bound)
- S3 upload: 5-10s (network-bound)

---

For more information, see:
- [README.md](../README.md) - Main documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Infrastructure details
- [QUICK_SETUP.md](../QUICK_SETUP.md) - Setup guide
