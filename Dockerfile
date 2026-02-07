# AI Music Generator - AWS Batch Docker Image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6"
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    git \
    wget \
    ca-certificates \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt requirements-full.txt requirements-aws.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements-full.txt

# Copy application code
COPY src/ ./src/
COPY models_config.yaml ./
COPY aws_batch_worker.py ./

# Create output directory
RUN mkdir -p /app/output

# Verify installation
RUN python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')" || echo "PyTorch check failed (expected in build)"

# Set entrypoint
ENTRYPOINT ["python3", "aws_batch_worker.py"]
