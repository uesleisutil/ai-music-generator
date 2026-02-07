#!/usr/bin/env python3
"""
Simplified pipeline without AI (for quick tests)
"""

from src.utils.upload_youtube import upload_video
from src.utils.create_video import create_video
from src.generators.generate_image_simple import generate_simple_image
from src.generators.generate_music_simple import generate_simple_music
import argparse
import os
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_simple_pipeline(prompt, duration=30, title=None, description="", tags=None, privacy="public", skip_upload=False):
    """Runs the simplified pipeline"""

    print("=" * 60)
    print("🚀 SIMPLIFIED PIPELINE (WITHOUT AI)")
    print("=" * 60)
    print("⚠️  This mode uses simple generators for quick tests")
    print("💡 For real AI, install: pip install -r requirements-full.txt")
    print("=" * 60)

    # 1. Generate music
    print("\n📍 STEP 1/4: Generating music...")
    music_path = generate_simple_music(prompt, duration, "output/music")

    # 2. Generate image
    print("\n📍 STEP 2/4: Generating cover image...")
    image_path = generate_simple_image(prompt, "output/cover.png")

    # 3. Create video
    print("\n📍 STEP 3/4: Creating video...")
    video_path = create_video(music_path, image_path, "output/video.mp4")

    # 4. Upload to YouTube (optional)
    if not skip_upload:
        print("\n📍 STEP 4/4: Uploading to YouTube...")
        video_title = title or f"{prompt.title()}"
        video_description = description or f"Test music: {prompt}\n\nGenerated with open-source tools."
        video_tags = tags or ["ai music", "test", "music"]

        try:
            video_url = upload_video(
                video_path,
                video_title,
                video_description,
                video_tags,
                privacy=privacy
            )
        except FileNotFoundError:
            print("⚠️  client_secrets.json not found")
            print("   Skipping upload. See SETUP.md to configure YouTube API")
            video_url = None
    else:
        print("\n📍 STEP 4/4: Upload skipped (--skip-upload)")
        video_url = None

    print("\n" + "=" * 60)
    print("🎉 PIPELINE COMPLETED!")
    print("=" * 60)
    print(f"🎵 Music: {music_path}")
    print(f"🎨 Image: {image_path}")
    print(f"🎬 Video: {video_path}")
    if video_url:
        print(f"🔗 YouTube: {video_url}")
    print("=" * 60)

    return video_path


def main():
    parser = argparse.ArgumentParser(description='Simplified pipeline (without AI)')
    parser.add_argument('--prompt', type=str, required=True, help='Music description')
    parser.add_argument('--duration', type=int, default=30, help='Duration in seconds')
    parser.add_argument('--title', type=str, help='Video title')
    parser.add_argument('--description', type=str, default='', help='Video description')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--privacy', type=str, default='public', choices=['public', 'private', 'unlisted'])
    parser.add_argument('--skip-upload', action='store_true', help='Skip YouTube upload')

    args = parser.parse_args()

    tags = args.tags.split(',') if args.tags else None

    run_simple_pipeline(
        args.prompt,
        args.duration,
        args.title,
        args.description,
        tags,
        args.privacy,
        args.skip_upload
    )


if __name__ == "__main__":
    main()
