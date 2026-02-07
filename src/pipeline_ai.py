#!/usr/bin/env python3
"""
Pipeline completo com múltiplos modelos de IA
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
    """Executa o pipeline com modelos de IA"""

    models_config = load_models_config()

    # Aplicar preset se especificado
    if preset:
        if preset not in models_config['presets']:
            print(f"❌ Preset '{preset}' não encontrado!")
            print(f"💡 Presets disponíveis: {', '.join(models_config['presets'].keys())}")
            return None

        preset_config = models_config['presets'][preset]
        music_model = music_model or preset_config['music']
        image_model = image_model or preset_config['image']
        print(f"\n🎯 Usando preset: {preset}")
        print(f"   {preset_config['description']}")

    # Usar modelos padrão se não especificado
    music_model = music_model or models_config['defaults']['music']
    image_model = image_model or models_config['defaults']['image']

    print("=" * 60)
    print("🚀 PIPELINE COM IA")
    print("=" * 60)
    print(f"🎵 Modelo de Música: {music_model}")
    print(f"🎨 Modelo de Imagem: {image_model}")
    print("=" * 60)

    # 1. Gerar música
    print("\n📍 ETAPA 1/4: Gerando música com IA...")
    music_path = generate_music_ai(prompt, duration, "output/music", music_model)

    if not music_path:
        print("❌ Falha ao gerar música")
        return None

    # 2. Gerar imagem
    print("\n📍 ETAPA 2/4: Gerando imagem de capa com IA...")
    image_path = generate_image_ai(prompt, "output/cover.png", image_model)

    if not image_path:
        print("❌ Falha ao gerar imagem")
        return None

    # 3. Criar vídeo
    print("\n📍 ETAPA 3/4: Criando vídeo...")
    video_path = create_video(music_path, image_path, "output/video.mp4")

    # 4. Upload para YouTube (opcional)
    video_url = None
    if not skip_upload:
        print("\n📍 ETAPA 4/4: Fazendo upload para YouTube...")
        video_title = title or f"{prompt.title()}"
        video_description = description or f"Música gerada por IA: {prompt}\n\nModelos: {music_model} + {image_model}"
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
            print("⚠️  client_secrets.json não encontrado")
            print("   Pulando upload. Veja SETUP.md para configurar YouTube API")
    else:
        print("\n📍 ETAPA 4/4: Upload pulado (--skip-upload)")

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
    parser = argparse.ArgumentParser(description='Pipeline completo com IA (múltiplos modelos)')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da música')
    parser.add_argument('--duration', type=int, default=30, help='Duração em segundos')
    parser.add_argument('--title', type=str, help='Título do vídeo')
    parser.add_argument('--description', type=str, default='', help='Descrição do vídeo')
    parser.add_argument('--tags', type=str, help='Tags separadas por vírgula')
    parser.add_argument('--privacy', type=str, default='public', choices=['public', 'private', 'unlisted'])
    parser.add_argument('--skip-upload', action='store_true', help='Pular upload para YouTube')
    parser.add_argument('--music-model', type=str, help='Modelo de música (veja list_models.py)')
    parser.add_argument('--image-model', type=str, help='Modelo de imagem (veja list_models.py)')
    parser.add_argument('--preset', type=str, choices=['quick', 'balanced', 'quality', 'experimental'],
                        help='Preset de modelos')

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
