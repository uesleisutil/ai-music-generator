#!/usr/bin/env python3
"""
Script to warm up GPU instance and keep it running for a specified duration.
After the duration, it automatically scales down to 0.
"""

import boto3
import time
import argparse
from datetime import datetime, timedelta


def warm_up_gpu(duration_minutes=60, profile='b3tr', region='us-east-1'):
    """Warm up GPU instance and schedule scale down"""
    
    compute_env = 'ai-music-generator-gpu-ondemand'
    desired_vcpus = 4  # 1 x g4dn.xlarge
    
    print("🔥 Warming up GPU instance...")
    print(f"   Compute Environment: {compute_env}")
    print(f"   Duration: {duration_minutes} minutes")
    print(f"   Profile: {profile}")
    print()
    
    # Create Batch client
    session = boto3.Session(profile_name=profile, region_name=region)
    batch = session.client('batch')
    
    # Update compute environment to request GPU instance
    print("⏳ Requesting GPU instance...")
    try:
        batch.update_compute_environment(
            computeEnvironment=compute_env,
            computeResources={
                'desiredVcpus': desired_vcpus
            }
        )
        print("✅ GPU instance requested (will provision in 3-5 minutes)")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print()
    print(f"💡 The instance will stay warm for {duration_minutes} minutes")
    print("   After that, it will automatically scale down to 0")
    print()
    
    # Calculate end time
    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    print(f"⏰ Will scale down at: {end_time.strftime('%H:%M:%S')}")
    print()
    print("🎵 Ready to process jobs!")
    print()
    
    # Wait for the duration
    print(f"⏳ Keeping instance warm... (Press Ctrl+C to scale down immediately)")
    try:
        remaining = duration_minutes * 60
        while remaining > 0:
            mins = remaining // 60
            secs = remaining % 60
            print(f"   Time remaining: {mins:02d}:{secs:02d}", end='\r')
            time.sleep(1)
            remaining -= 1
        
        print()
        print()
        print("⏰ Duration elapsed, scaling down...")
        
    except KeyboardInterrupt:
        print()
        print()
        print("⚠️  Interrupted by user, scaling down...")
    
    # Scale down
    try:
        batch.update_compute_environment(
            computeEnvironment=compute_env,
            computeResources={
                'desiredVcpus': 0
            }
        )
        print("✅ GPU instance scaled down to 0")
        print("   Instance will terminate when no jobs are running")
    except Exception as e:
        print(f"❌ Error scaling down: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Warm up GPU instance for faster job execution'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Duration to keep instance warm (minutes, default: 60)'
    )
    parser.add_argument(
        '--profile',
        type=str,
        default='b3tr',
        help='AWS profile name (default: b3tr)'
    )
    parser.add_argument(
        '--region',
        type=str,
        default='us-east-1',
        help='AWS region (default: us-east-1)'
    )
    
    args = parser.parse_args()
    
    warm_up_gpu(
        duration_minutes=args.duration,
        profile=args.profile,
        region=args.region
    )


if __name__ == '__main__':
    main()
