#!/usr/bin/env python3
"""
Gerador de música simples usando síntese de áudio
(Versão sem IA para testes rápidos)
"""

import argparse
import os
import yaml
import numpy as np
from scipy.io import wavfile


def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def generate_simple_music(prompt, duration=30, output_path="output/music"):
    """
    Gera música simples usando síntese de áudio
    NOTA: Esta é uma versão simplificada para testes.
    Para música real com IA, instale audiocraft: pip install audiocraft
    """
    print(f"⚠️  Usando gerador simples (sem IA)")
    print(f"🎵 Gerando música de teste: '{prompt}' ({duration}s)...")

    # Parâmetros
    sample_rate = 44100
    num_samples = int(sample_rate * duration)

    # Gerar tons baseados no prompt
    if "lofi" in prompt.lower() or "chill" in prompt.lower():
        # Tons suaves e relaxantes
        frequencies = [261.63, 329.63, 392.00, 523.25]  # C, E, G, C (acorde C maior)
        tempo = 0.5
    elif "energetic" in prompt.lower() or "upbeat" in prompt.lower():
        frequencies = [440.00, 554.37, 659.25, 880.00]  # A, C#, E, A
        tempo = 0.25
    elif "jazz" in prompt.lower():
        frequencies = [293.66, 369.99, 440.00, 554.37]  # D, F#, A, C#
        tempo = 0.4
    else:
        # Padrão
        frequencies = [261.63, 293.66, 329.63, 349.23]  # C, D, E, F
        tempo = 0.5

    # Criar áudio
    audio = np.zeros(num_samples)
    t = np.linspace(0, duration, num_samples)

    # Adicionar múltiplas frequências com envelope
    for i, freq in enumerate(frequencies):
        # Onda senoidal
        wave = np.sin(2 * np.pi * freq * t)

        # Envelope ADSR simplificado
        attack = int(0.1 * sample_rate)
        decay = int(0.2 * sample_rate)
        sustain_level = 0.7
        release = int(0.3 * sample_rate)

        envelope = np.ones(num_samples)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[attack:attack + decay] = np.linspace(1, sustain_level, decay)
        envelope[-release:] = np.linspace(sustain_level, 0, release)

        # Aplicar envelope e adicionar ao áudio
        audio += wave * envelope * (0.3 / len(frequencies))

    # Normalizar
    audio = audio / np.max(np.abs(audio)) * 0.8

    # Converter para int16
    audio_int16 = (audio * 32767).astype(np.int16)

    # Criar diretório de saída
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    # Salvar arquivo
    output_file = f"{output_path}.wav"
    print(f"💾 Salvando música em {output_file}...")
    wavfile.write(output_file, sample_rate, audio_int16)

    print(f"✅ Música de teste gerada!")
    print(f"💡 Para música real com IA, instale: pip install torch audiocraft")

    return output_file


def main():
    parser = argparse.ArgumentParser(description='Gerar música simples (sem IA)')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da música')
    parser.add_argument('--duration', type=int, default=30, help='Duração em segundos')
    parser.add_argument('--output', type=str, default='output/music', help='Caminho de saída')

    args = parser.parse_args()

    generate_simple_music(args.prompt, args.duration, args.output)


if __name__ == "__main__":
    main()
