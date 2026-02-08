#!/usr/bin/env python3
"""
Create video combining music and image using FFmpeg
"""

import argparse
import subprocess
import os


def create_video(audio_path, image_path, output_path="output/video.mp4"):
    """Combine audio and image into a video"""

    print("🎬 Creating video...")
    print(f"   Audio: {audio_path}")
    print(f"   Image: {image_path}")

    # Create output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # FFmpeg command to create video
    command = [
        "ffmpeg",
        "-loop",
        "1",  # Loop the image
        "-i",
        image_path,  # Input image
        "-i",
        audio_path,  # Input audio
        "-c:v",
        "libx264",  # Video codec
        "-tune",
        "stillimage",  # Optimization for static image
        "-c:a",
        "aac",  # Audio codec
        "-b:a",
        "192k",  # Audio bitrate
        "-pix_fmt",
        "yuv420p",  # Pixel format (compatibility)
        "-shortest",  # Duration = audio duration
        "-y",  # Overwrite existing file
        output_path,
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
        print(f"✅ Video created successfully: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating video: {e.stderr.decode()}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Create video from audio and image")
    parser.add_argument("--audio", type=str, required=True, help="Audio file path")
    parser.add_argument("--image", type=str, required=True, help="Image path")
    parser.add_argument("--output", type=str, default="output/video.mp4", help="Output path")

    args = parser.parse_args()

    create_video(args.audio, args.image, args.output)


if __name__ == "__main__":
    main()
