#!/usr/bin/env python3
"""
Example: Generate multiple videos in batch on AWS
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_submit_job import submit_job
import time

# Configuration
OUTPUT_BUCKET = "your-bucket-name"  # Change this!
PRESET = "balanced"

# List of prompts to generate
prompts = [
    {"prompt": "cozy lofi coffee shop music with rain sounds", "duration": 60},
    {"prompt": "peaceful forest ambience with birds chirping", "duration": 45},
    {"prompt": "upbeat electronic music for studying", "duration": 60},
    {"prompt": "relaxing piano music for meditation", "duration": 90},
    {"prompt": "energetic synthwave music for gaming", "duration": 60},
]


def main():
    print("\n" + "=" * 60)
    print("🎵 BATCH MUSIC GENERATION")
    print("=" * 60)
    print(f"Total jobs: {len(prompts)}")
    print(f"Output bucket: {OUTPUT_BUCKET}")
    print(f"Preset: {PRESET}")
    print("=" * 60 + "\n")

    if OUTPUT_BUCKET == "your-bucket-name":
        print("❌ Error: Please set OUTPUT_BUCKET in this script!")
        return

    submitted_jobs = []

    # Submit all jobs
    for i, job_config in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] Submitting job...")
        print(f"   Prompt: {job_config['prompt']}")
        print(f"   Duration: {job_config['duration']}s")

        try:
            result = submit_job(
                prompt=job_config["prompt"],
                duration=job_config["duration"],
                preset=PRESET,
                output_bucket=OUTPUT_BUCKET,
                wait=False,
            )

            submitted_jobs.append(result)
            print(f"   ✅ Submitted: {result['batch_job_id']}")

            # Small delay to avoid rate limiting
            time.sleep(1)

        except Exception as e:
            print(f"   ❌ Failed: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 BATCH SUBMISSION COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully submitted: {len(submitted_jobs)}/{len(prompts)} jobs")
    print()

    if submitted_jobs:
        print("📋 Job IDs:")
        for job in submitted_jobs:
            print(f"   - {job['job_id']}: {job['batch_job_id']}")

        print()
        print("💡 To check status:")
        print("   aws batch list-jobs --job-queue ai-music-generator-queue --job-status RUNNING")
        print()
        print("💡 To view logs:")
        print("   aws logs tail /aws/batch/ai-music-generator --follow")
        print()
        print("💡 To download results:")
        for job in submitted_jobs:
            print(f"   aws s3 sync {job['output_location']} ./downloads/{job['job_id']}/")
        print()


if __name__ == "__main__":
    main()
