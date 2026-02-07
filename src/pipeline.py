#!/usr/bin/env python3
"""
Pipeline completo: gera música, imagem, vídeo e faz upload no YouTube
"""

from src.utils.upload_youtube import upload_video
from src.utils.create_video import create_video
from src.generators.generate_image import generate_image
from src.generators.generate_music import generate_music
import argparse
import os
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_pipeline(prompt, duration=30, title=None, description="", tags=None, privacy="public"):
    """Executa o pipeline completo"""

    print("=" * 60)
    print("🚀 INICIANDO PIPELINE DE GERAÇÃO E UPLOAD")
    print("=" * 60)

    # 1. Gerar música
    print("\n📍 STEP 1/4: Generating music...")
    music_path = generate_music(prompt, duration, "output/music")

    # 2. Gerar imagem
    print("\n📍 STEP 2/4: Generating cover image...")
    image_path = generate_image(prompt, "output/cover.png")

    # 3. Criar vídeo
    print("\n📍 STEP 3/4: Creating video...")
    video_path = create_video(music_path, image_path, "output/video.mp4")

    # 4. Upload para YouTube
    print("\n📍 STEP 4/4: Uploading to YouTube...")
    video_title = title or f"{prompt.title()}"
    video_description = description or f"Music gerada por IA: {prompt}\n\nGerado com ferramentas open-source."
    video_tags = tags or ["ai music", "lofi", "music", "ai generated"]

    video_url = upload_video(
        video_path,
        video_title,
        video_description,
        video_tags,
        privacy=privacy
    )

    print("\n" + "=" * 60)
    print("🎉 PIPELINE COMPLETED COM SUCESSO!")
    print("=" * 60)
    print(f"🎵 Music: {music_path}")
    print(f"🎨 Image: {image_path}")
    print(f"🎬 Video: {video_path}")
    print(f"🔗 YouTube: {video_url}")
    print("=" * 60)

    return video_url


def main():
    parser = argparse.ArgumentParser(description='Pipeline completo de geração e upload')
    parser.add_argument('--prompt', type=str, required=True, help='Music description (ex: "cozy lofi home music")')
    parser.add_argument('--duration', type=int, default=30, help='Duração da música em segundos')
    parser.add_argument('--title', type=str, help='Video title no YouTube')
    parser.add_argument('--description', type=str, default='', help='Video description')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--privacy', type=str, default='public', choices=['public', 'private', 'unlisted'])

    args = parser.parse_args()

    tags = args.tags.split(',') if args.tags else None

    run_pipeline(
        args.prompt,
        args.duration,
        args.title,
        args.description,
        tags,
        args.privacy
    )


if __name__ == "__main__":
    main()
