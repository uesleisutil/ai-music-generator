# AI Music Generator - AWS Batch Docker Image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements-full.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements-full.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /app/output

# Set entrypoint
ENTRYPOINT ["python3", "aws_batch_worker.py"]
