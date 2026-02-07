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
    print("\n📍 ETAPA 1/4: Gerando música...")
    music_path = generate_music(prompt, duration, "output/music")

    # 2. Gerar imagem
    print("\n📍 ETAPA 2/4: Gerando imagem de capa...")
    image_path = generate_image(prompt, "output/cover.png")

    # 3. Criar vídeo
    print("\n📍 ETAPA 3/4: Criando vídeo...")
    video_path = create_video(music_path, image_path, "output/video.mp4")

    # 4. Upload para YouTube
    print("\n📍 ETAPA 4/4: Fazendo upload para YouTube...")
    video_title = title or f"{prompt.title()}"
    video_description = description or f"Música gerada por IA: {prompt}\n\nGerado com ferramentas open-source."
    video_tags = tags or ["ai music", "lofi", "music", "ai generated"]

    video_url = upload_video(
        video_path,
        video_title,
        video_description,
        video_tags,
        privacy=privacy
    )

    print("\n" + "=" * 60)
    print("🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print(f"🎵 Música: {music_path}")
    print(f"🎨 Imagem: {image_path}")
    print(f"🎬 Vídeo: {video_path}")
    print(f"🔗 YouTube: {video_url}")
    print("=" * 60)

    return video_url


def main():
    parser = argparse.ArgumentParser(description='Pipeline completo de geração e upload')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da música (ex: "cozy lofi home music")')
    parser.add_argument('--duration', type=int, default=30, help='Duração da música em segundos')
    parser.add_argument('--title', type=str, help='Título do vídeo no YouTube')
    parser.add_argument('--description', type=str, default='', help='Descrição do vídeo')
    parser.add_argument('--tags', type=str, help='Tags separadas por vírgula')
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
