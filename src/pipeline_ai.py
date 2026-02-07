#!/usr/bin/env python3
"""
Complete pipeline with multiple AI models
"""

from src.utils.upload_youtube import upload_video
from src.utils.create_video import create_video
from src.generators.generate_image_ai import generate_image_ai
from src.generators.generate_music_ai import generate_music_ai
import argparse
import os
import yaml
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_models_config():
    with open('models_config.yaml', 'r') as f:
        return yaml.safe_load(f)


def run_ai_pipeline(prompt, duration=30, title=None, description="", tags=None,
                    privacy="public", skip_upload=False, music_model=None,
                    image_model=None, preset=None):
    """Runs the pipeline with AI models"""

    models_config = load_models_config()

    # Aplicar preset se especificado
    if preset:
        if preset not in models_config['presets']:
            print(f"❌ Preset '{preset}' not found!")
            print(f"💡 Available presets: {', '.join(models_config['presets'].keys())}")
            return None

        preset_config = models_config['presets'][preset]
        music_model = music_model or preset_config['music']
        image_model = image_model or preset_config['image']
        print(f"\n🎯 Using preset: {preset}")
        print(f"   {preset_config['description']}")

    # Usar models padrão se não especificado
    music_model = music_model or models_config['defaults']['music']
    image_model = image_model or models_config['defaults']['image']

    print("=" * 60)
    print("🚀 PIPELINE WITH AI")
    print("=" * 60)
    print(f"🎵 Model de Music: {music_model}")
    print(f"🎨 Model de Image: {image_model}")
    print("=" * 60)

    # 1. Gerar music
    print("\n📍 STEP 1/4: Generating music with AI...")
    music_path = generate_music_ai(prompt, duration, "output/music", music_model)

    if not music_path:
        print("❌ Failed to generate music")
        return None

    # 2. Gerar image
    print("\n📍 STEP 2/4: Generating cover image with AI...")
    image_path = generate_image_ai(prompt, "output/cover.png", image_model)

    if not image_path:
        print("❌ Failed to generate image")
        return None

    # 3. Criar vídeo
    print("\n📍 STEP 3/4: Creating video...")
    video_path = create_video(music_path, image_path, "output/video.mp4")

    # 4. Upload para YouTube (opcional)
    video_url = None
    if not skip_upload:
        print("\n📍 STEP 4/4: Uploading to YouTube...")
        video_title = title or f"{prompt.title()}"
        video_description = description or f"Music generated por IA: {prompt}\n\nModels: {music_model} + {image_model}"
        video_tags = tags or ["ai music", "ai generated", "music"]

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
            print("   Skipping upload. Veja SETUP.md to configure YouTube API")
    else:
        print("\n📍 STEP 4/4: Upload skipped (--skip-upload)")

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
    parser = argparse.ArgumentParser(description='Complete pipeline with AI (múltiplos models)')
    parser.add_argument('--prompt', type=str, required=True, help='Music description')
    parser.add_argument('--duration', type=int, default=30, help='Duration in seconds')
    parser.add_argument('--title', type=str, help='Video title')
    parser.add_argument('--description', type=str, default='', help='Video description')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--privacy', type=str, default='public', choices=['public', 'private', 'unlisted'])
    parser.add_argument('--skip-upload', action='store_true', help='Skip YouTube upload')
    parser.add_argument('--music-model', type=str, help='Model de music (see list_models.py)')
    parser.add_argument('--image-model', type=str, help='Model de image (see list_models.py)')
    parser.add_argument('--preset', type=str, choices=['quick', 'balanced', 'quality', 'experimental'],
                        help='Model preset')

    args = parser.parse_args()

    tags = args.tags.split(',') if args.tags else None

    run_ai_pipeline(
        args.prompt,
        args.duration,
        args.title,
        args.description,
        tags,
        args.privacy,
        args.skip_upload,
        args.music_model,
        args.image_model,
        args.preset
    )


if __name__ == "__main__":
    main()
