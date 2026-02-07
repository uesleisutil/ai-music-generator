#!/usr/bin/env python3
"""
Gerador de música usando MusicGen (Meta)
"""

import argparse
import os
import yaml
import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write


def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def generate_music(prompt, duration=30, output_path="output/music"):
    """Gera música baseada no prompt"""
    config = load_config()

    print(f"🎵 Carregando modelo MusicGen ({config['music']['model']})...")
    model = MusicGen.get_pretrained(config['music']['model'])

    # Configurar duração
    model.set_generation_params(duration=duration)

    print(f"🎼 Generating music: '{prompt}'...")
    descriptions = [prompt]

    # Gerar música
    wav = model.generate(descriptions)

    # Criar diretório de saída
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    # Salvar arquivo
    print(f"💾 Saving music to {output_path}.wav...")
    audio_write(
        output_path,
        wav[0].cpu(),
        model.sample_rate,
        strategy="loudness",
        loudness_compressor=True
    )

    print(f"✅ Music gerada com sucesso!")
    return f"{output_path}.wav"


def main():
    parser = argparse.ArgumentParser(description='Gerar música com IA')
    parser.add_argument('--prompt', type=str, required=True, help='Music description')
    parser.add_argument('--duration', type=int, default=30, help='Duration in seconds')
    parser.add_argument('--output', type=str, default='output/music', help='Caminho de saída')

    args = parser.parse_args()

    generate_music(args.prompt, args.duration, args.output)


if __name__ == "__main__":
    main()
