#!/usr/bin/env python3
"""
Pipeline simplificado sem IA (para testes rápidos)
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
    """Executa o pipeline simplificado"""

    print("=" * 60)
    print("🚀 PIPELINE SIMPLIFICADO (SEM IA)")
    print("=" * 60)
    print("⚠️  Este modo usa geradores simples para testes rápidos")
    print("💡 Para IA real, instale: pip install -r requirements-full.txt")
    print("=" * 60)

    # 1. Gerar música
    print("\n📍 ETAPA 1/4: Gerando música...")
    music_path = generate_simple_music(prompt, duration, "output/music")

    # 2. Gerar imagem
    print("\n📍 ETAPA 2/4: Gerando imagem de capa...")
    image_path = generate_simple_image(prompt, "output/cover.png")

    # 3. Criar vídeo
    print("\n📍 ETAPA 3/4: Criando vídeo...")
    video_path = create_video(music_path, image_path, "output/video.mp4")

    # 4. Upload para YouTube (opcional)
    if not skip_upload:
        print("\n📍 ETAPA 4/4: Fazendo upload para YouTube...")
        video_title = title or f"{prompt.title()}"
        video_description = description or f"Música de teste: {prompt}\n\nGerado com ferramentas open-source."
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
            print("⚠️  client_secrets.json não encontrado")
            print("   Pulando upload. Veja SETUP.md para configurar YouTube API")
            video_url = None
    else:
        print("\n📍 ETAPA 4/4: Upload pulado (--skip-upload)")
        video_url = None

    print("\n" + "=" * 60)
    print("🎉 PIPELINE CONCLUÍDO!")
    print("=" * 60)
    print(f"🎵 Música: {music_path}")
    print(f"🎨 Imagem: {image_path}")
    print(f"🎬 Vídeo: {video_path}")
    if video_url:
        print(f"🔗 YouTube: {video_url}")
    print("=" * 60)

    return video_path


def main():
    parser = argparse.ArgumentParser(description='Pipeline simplificado (sem IA)')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da música')
    parser.add_argument('--duration', type=int, default=30, help='Duração em segundos')
    parser.add_argument('--title', type=str, help='Título do vídeo')
    parser.add_argument('--description', type=str, default='', help='Descrição do vídeo')
    parser.add_argument('--tags', type=str, help='Tags separadas por vírgula')
    parser.add_argument('--privacy', type=str, default='public', choices=['public', 'private', 'unlisted'])
    parser.add_argument('--skip-upload', action='store_true', help='Pular upload para YouTube')

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
