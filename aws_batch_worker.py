#!/usr/bin/env python3
"""
AWS Batch Worker - Processes music generation jobs in the cloud
"""

import os
import sys
import json
import boto3
import argparse
from datetime import datetime

# Import pipeline
from src.pipeline_ai import run_pipeline_ai


def download_from_s3(bucket, key, local_path):
    """Download file from S3"""
    s3 = boto3.client('s3')
    print(f"📥 Downloading s3://{bucket}/{key} to {local_path}")
    s3.download_file(bucket, key, local_path)
    print(f"✅ Download complete")


def upload_to_s3(local_path, bucket, key):
    """Upload file to S3"""
    s3 = boto3.client('s3')
    print(f"📤 Uploading {local_path} to s3://{bucket}/{key}")
    s3.upload_file(local_path, bucket, key)
    print(f"✅ Upload complete: s3://{bucket}/{key}")


def process_job(job_config):
    """Process a single music generation job"""
    
    print("\n" + "="*60)
    print("🎵 AWS BATCH - AI MUSIC GENERATOR")
    print("="*60)
    print(f"Job ID: {job_config.get('job_id', 'unknown')}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*60 + "\n")
    
    # Extract job parameters
    prompt = job_config['prompt']
    duration = job_config.get('duration', 30)
    preset = job_config.get('preset', 'balanced')
    resolution = job_config.get('resolution', 'hd')
    output_bucket = job_config['output_bucket']
    output_prefix = job_config.get('output_prefix', 'output')
    job_id = job_config.get('job_id', datetime.now().strftime('%Y%m%d_%H%M%S'))
    
    print(f"📝 Prompt: {prompt}")
    print(f"⏱️  Duration: {duration}s")
    print(f"🎯 Preset: {preset}")
    print(f"📐 Resolution: {resolution.upper()}")
    print(f"📦 Output: s3://{output_bucket}/{output_prefix}/{job_id}/")
    print()
    
    # Set local output path
    local_output_dir = f"/app/output/{job_id}"
    os.makedirs(local_output_dir, exist_ok=True)
    local_output_base = f"{local_output_dir}/output"
    
    # Run the AI pipeline
    print("🚀 Starting AI pipeline...\n")
    
    try:
        result = run_pipeline_ai(
            prompt=prompt,
            duration=duration,
            output_path=local_output_base,
            preset=preset,
            resolution=resolution,
            skip_upload=True  # We'll upload to S3 instead
        )
        
        if not result:
            raise Exception("Pipeline failed to generate output")
        
        print("\n✅ Pipeline completed successfully!")
        
        # Upload results to S3
        print("\n" + "="*60)
        print("📤 Uploading results to S3...")
        print("="*60 + "\n")
        
        files_to_upload = [
            ('music.wav', f"{local_output_base}.wav"),
            ('cover.png', f"{local_output_base}.png"),
            ('video.mp4', f"{local_output_base}.mp4")
        ]
        
        uploaded_files = {}
        
        for file_type, local_file in files_to_upload:
            if os.path.exists(local_file):
                s3_key = f"{output_prefix}/{job_id}/{file_type}"
                upload_to_s3(local_file, output_bucket, s3_key)
                uploaded_files[file_type] = f"s3://{output_bucket}/{s3_key}"
            else:
                print(f"⚠️  Warning: {local_file} not found, skipping upload")
        
        # Create and upload job metadata
        metadata = {
            'job_id': job_id,
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'duration': duration,
            'preset': preset,
            'files': uploaded_files
        }
        
        metadata_file = f"{local_output_dir}/metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        metadata_key = f"{output_prefix}/{job_id}/metadata.json"
        upload_to_s3(metadata_file, output_bucket, metadata_key)
        
        print("\n" + "="*60)
        print("🎉 JOB COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📦 Results available at:")
        for file_type, s3_path in uploaded_files.items():
            print(f"   {file_type}: {s3_path}")
        print(f"   metadata: s3://{output_bucket}/{metadata_key}")
        print()
        
        return metadata
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Upload error metadata
        error_metadata = {
            'job_id': job_id,
            'status': 'failed',
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'prompt': prompt
        }
        
        error_file = f"{local_output_dir}/error.json"
        with open(error_file, 'w') as f:
            json.dump(error_metadata, f, indent=2)
        
        try:
            error_key = f"{output_prefix}/{job_id}/error.json"
            upload_to_s3(error_file, output_bucket, error_key)
        except:
            pass
        
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='AWS Batch Worker for AI Music Generation')
    parser.add_argument('--job-config', type=str, help='Path to job config JSON file')
    parser.add_argument('--job-config-s3', type=str, help='S3 path to job config (s3://bucket/key)')
    parser.add_argument('--prompt', type=str, help='Music prompt')
    parser.add_argument('--duration', type=int, default=30, help='Duration in seconds')
    parser.add_argument('--preset', type=str, default='balanced', help='Quality preset')
    parser.add_argument('--resolution', type=str, default='hd', 
                        choices=['hd', 'fhd', '2k', '4k', 'youtube'],
                        help='Video resolution')
    parser.add_argument('--output-bucket', type=str, help='S3 bucket for output')
    parser.add_argument('--output-prefix', type=str, default='output', help='S3 prefix for output')
    
    args = parser.parse_args()
    
    # Load job configuration
    if args.job_config:
        # Load from local file
        with open(args.job_config, 'r') as f:
            job_config = json.load(f)
    elif args.job_config_s3:
        # Download from S3
        parts = args.job_config_s3.replace('s3://', '').split('/', 1)
        bucket = parts[0]
        key = parts[1]
        local_config = '/tmp/job_config.json'
        download_from_s3(bucket, key, local_config)
        with open(local_config, 'r') as f:
            job_config = json.load(f)
    else:
        # Build from command line arguments
        if not args.prompt or not args.output_bucket:
            print("❌ Error: --prompt and --output-bucket are required")
            sys.exit(1)
        
        job_config = {
            'job_id': os.environ.get('AWS_BATCH_JOB_ID', datetime.now().strftime('%Y%m%d_%H%M%S')),
            'prompt': args.prompt,
            'duration': args.duration,
            'preset': args.preset,
            'resolution': args.resolution,
            'output_bucket': args.output_bucket,
            'output_prefix': args.output_prefix
        }
    
    # Process the job
    process_job(job_config)


if __name__ == "__main__":
    main()
