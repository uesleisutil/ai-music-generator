#!/usr/bin/env python3
"""
Cria vídeo combinando música e imagem usando FFmpeg
"""

import argparse
import subprocess
import os

def create_video(audio_path, image_path, output_path="output/video.mp4"):
    """Combina áudio e imagem em um vídeo"""

    print(f"🎬 Creating video...")
    print(f"   Áudio: {audio_path}")
    print(f"   Image: {image_path}")

    # Criar diretório de saída
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Comando FFmpeg para criar vídeo
    command = [
        'ffmpeg',
        '-loop', '1',  # Loop na imagem
        '-i', image_path,  # Image de entrada
        '-i', audio_path,  # Áudio de entrada
        '-c:v', 'libx264',  # Codec de vídeo
        '-tune', 'stillimage',  # Otimização para imagem estática
        '-c:a', 'aac',  # Codec de áudio
        '-b:a', '192k',  # Bitrate do áudio
        '-pix_fmt', 'yuv420p',  # Formato de pixel (compatibilidade)
        '-shortest',  # Duração = duração do áudio
        '-y',  # Sobrescrever arquivo existente
        output_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
        print(f"✅ Video criado com sucesso: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar vídeo: {e.stderr.decode()}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Criar vídeo a partir de áudio e imagem')
    parser.add_argument('--audio', type=str, required=True, help='Caminho do arquivo de áudio')
    parser.add_argument('--image', type=str, required=True, help='Caminho da imagem')
    parser.add_argument('--output', type=str, default='output/video.mp4', help='Caminho de saída')

    args = parser.parse_args()

    create_video(args.audio, args.image, args.output)

if __name__ == "__main__":
    main()
