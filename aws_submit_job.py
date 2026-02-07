#!/usr/bin/env python3
"""
Submit jobs to AWS Batch for processing
"""

import boto3
import json
import argparse
from datetime import datetime
import time


def submit_job(
    prompt,
    duration=30,
    preset='balanced',
    resolution='hd',
    use_bedrock=True,
    bedrock_model='sdxl',
    job_queue='ai-music-generator-queue',
    job_definition='ai-music-generator-job',
    output_bucket=None,
    output_prefix='output',
    wait=False
):
    """Submit a job to AWS Batch"""
    
    if not output_bucket:
        raise ValueError("output_bucket is required")
    
    # Generate job ID
    job_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    job_name = f"music-gen-{job_id}"
    
    # Create job configuration
    job_config = {
        'job_id': job_id,
        'prompt': prompt,
        'duration': duration,
        'preset': preset,
        'resolution': resolution,
        'use_bedrock': use_bedrock,
        'bedrock_model': bedrock_model,
        'output_bucket': output_bucket,
        'output_prefix': output_prefix
    }
    
    print("\n" + "="*60)
    print("🚀 SUBMITTING JOB TO AWS BATCH")
    print("="*60)
    print(f"Job Name: {job_name}")
    print(f"Job ID: {job_id}")
    print(f"Prompt: {prompt}")
    print(f"Duration: {duration}s")
    print(f"Preset: {preset}")
    print(f"Resolution: {resolution.upper()}")
    print(f"Image Generator: {'AWS Bedrock (' + bedrock_model.upper() + ')' if use_bedrock else 'Local Models'}")
    print(f"Output: s3://{output_bucket}/{output_prefix}/{job_id}/")
    print("="*60 + "\n")
    
    # Submit to AWS Batch
    batch = boto3.client('batch')
    
    try:
        response = batch.submit_job(
            jobName=job_name,
            jobQueue=job_queue,
            jobDefinition=job_definition,
            containerOverrides={
                'command': [
                    '--prompt', prompt,
                    '--duration', str(duration),
                    '--preset', preset,
                    '--resolution', resolution,
                    '--use-bedrock' if use_bedrock else '--no-use-bedrock',
                    '--bedrock-model', bedrock_model,
                    '--output-bucket', output_bucket,
                    '--output-prefix', output_prefix
                ]
            }
        )
        
        batch_job_id = response['jobId']
        
        print(f"✅ Job submitted successfully!")
        print(f"   AWS Batch Job ID: {batch_job_id}")
        print(f"   Job Name: {job_name}")
        print()
        
        if wait:
            print("⏳ Waiting for job to complete...")
            print("   (This may take 5-10 minutes)")
            print()
            
            while True:
                job_desc = batch.describe_jobs(jobs=[batch_job_id])['jobs'][0]
                status = job_desc['status']
                
                print(f"   Status: {status}", end='\r')
                
                if status in ['SUCCEEDED', 'FAILED']:
                    print()
                    break
                
                time.sleep(10)
            
            if status == 'SUCCEEDED':
                print(f"\n🎉 Job completed successfully!")
                print(f"\n📦 Results available at:")
                print(f"   s3://{output_bucket}/{output_prefix}/{job_id}/")
                print()
                
                # List output files
                s3 = boto3.client('s3')
                try:
                    objects = s3.list_objects_v2(
                        Bucket=output_bucket,
                        Prefix=f"{output_prefix}/{job_id}/"
                    )
                    
                    if 'Contents' in objects:
                        print("   Files:")
                        for obj in objects['Contents']:
                            key = obj['Key']
                            size = obj['Size']
                            print(f"   - {key} ({size:,} bytes)")
                except Exception as e:
                    print(f"   (Could not list files: {e})")
                
            else:
                print(f"\n❌ Job failed!")
                print(f"   Check CloudWatch logs for details")
        else:
            print(f"💡 To check job status:")
            print(f"   aws batch describe-jobs --jobs {batch_job_id}")
            print()
            print(f"💡 To view logs:")
            print(f"   Check CloudWatch Logs: /aws/batch/job")
            print()
        
        return {
            'job_id': job_id,
            'batch_job_id': batch_job_id,
            'job_name': job_name,
            'output_location': f"s3://{output_bucket}/{output_prefix}/{job_id}/"
        }
        
    except Exception as e:
        print(f"❌ Error submitting job: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description='Submit AI Music Generation job to AWS Batch')
    parser.add_argument('--prompt', type=str, required=True, help='Music description')
    parser.add_argument('--duration', type=int, default=30, help='Duration in seconds')
    parser.add_argument('--preset', type=str, default='balanced', 
                       choices=['quick', 'balanced', 'quality', 'experimental'],
                       help='Quality preset')
    parser.add_argument('--resolution', type=str, default='hd',
                       choices=['hd', 'fhd', '2k', '4k', 'youtube'],
                       help='Video resolution: hd (720p), fhd (1080p), 2k (1440p), 4k (2160p)')
    parser.add_argument('--use-bedrock', action='store_true', default=True,
                       help='Use AWS Bedrock for image generation (default: True, better quality)')
    parser.add_argument('--bedrock-model', type=str, default='sdxl', choices=['sdxl', 'titan'],
                       help='Bedrock model: sdxl (Stable Diffusion XL) or titan (Amazon Titan)')
    parser.add_argument('--output-bucket', type=str, required=True, help='S3 bucket for output')
    parser.add_argument('--output-prefix', type=str, default='output', help='S3 prefix for output')
    parser.add_argument('--job-queue', type=str, default='ai-music-generator-queue', 
                       help='AWS Batch job queue name')
    parser.add_argument('--job-definition', type=str, default='ai-music-generator-job',
                       help='AWS Batch job definition name')
    parser.add_argument('--wait', action='store_true', help='Wait for job to complete')
    
    args = parser.parse_args()
    
    result = submit_job(
        prompt=args.prompt,
        duration=args.duration,
        preset=args.preset,
        resolution=args.resolution,
        use_bedrock=args.use_bedrock,
        bedrock_model=args.bedrock_model,
        job_queue=args.job_queue,
        job_definition=args.job_definition,
        output_bucket=args.output_bucket,
        output_prefix=args.output_prefix,
        wait=args.wait
    ) 
                       choices=['quick', 'balanced', 'quality', 'experimental'],
                       help='Quality preset')
    parser.add_argument('--output-bucket', type=str, required=True, help='S3 bucket for output')
    parser.add_argument('--output-prefix', type=str, default='output', help='S3 prefix for output')
    parser.add_argument('--job-queue', type=str, default='ai-music-generator-queue', 
                       help='AWS Batch job queue name')
    parser.add_argument('--job-definition', type=str, default='ai-music-generator-job',
                       help='AWS Batch job definition name')
    parser.add_argument('--wait', action='store_true', help='Wait for job to complete')
    
    args = parser.parse_args()
    
    result = submit_job(
        prompt=args.prompt,
        duration=args.duration,
        preset=args.preset,
        job_queue=args.job_queue,
        job_definition=args.job_definition,
        output_bucket=args.output_bucket,
        output_prefix=args.output_prefix,
        wait=args.wait
    )
    
    # Save job info
    job_info_file = f"job_{result['job_id']}.json"
    with open(job_info_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"💾 Job info saved to: {job_info_file}")
    print()


if __name__ == "__main__":
    main()
