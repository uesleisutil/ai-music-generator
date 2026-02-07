#!/usr/bin/env python3
"""
Gerador de música usando múltiplos modelos de IA
"""

import argparse
import os
import yaml
import torch

def load_models_config():
    with open('models_config.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def generate_with_musicgen(model_id, prompt, duration, output_path):
    """Gera música usando MusicGen"""
    from audiocraft.models import MusicGen
    from audiocraft.data.audio import audio_write
    
    print(f"🎵 Carregando MusicGen ({model_id})...")
    model = MusicGen.get_pretrained(model_id)
    model.set_generation_params(duration=duration)
    
    print(f"🎼 Gerando música: '{prompt}'...")
    wav = model.generate([prompt])
    
    print(f"💾 Salvando música...")
    audio_write(output_path, wav[0].cpu(), model.sample_rate, strategy="loudness")
    
    return f"{output_path}.wav"

def generate_with_audioldm(model_id, prompt, duration, output_path):
    """Gera música usando AudioLDM"""
    from diffusers import AudioLDMPipeline
    
    print(f"🎵 Carregando AudioLDM ({model_id})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = AudioLDMPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
    pipe = pipe.to(device)
    
    print(f"🎼 Gerando música: '{prompt}'...")
    audio = pipe(
        prompt,
        num_inference_steps=50,
        audio_length_in_s=duration
    ).audios[0]
    
    # Salvar áudio
    import scipy.io.wavfile as wavfile
    sample_rate = 16000
    output_file = f"{output_path}.wav"
    wavfile.write(output_file, sample_rate, audio)
    
    print(f"💾 Música salva em {output_file}")
    return output_file

def generate_with_riffusion(model_id, prompt, duration, output_path):
    """Gera música usando Riffusion"""
    from diffusers import StableDiffusionPipeline
    import numpy as np
    from PIL import Image
    
    print(f"🎵 Carregando Riffusion ({model_id})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
    pipe = pipe.to(device)
    
    print(f"🎼 Gerando espectrograma: '{prompt}'...")
    # Riffusion gera espectrogramas que são convertidos em áudio
    image = pipe(prompt).images[0]
    
    # Converter espectrograma para áudio (simplificado)
    # Em produção, use a biblioteca riffusion completa
    print(f"⚠️  Riffusion requer conversão adicional de espectrograma para áudio")
    print(f"💡 Use MusicGen ou AudioLDM para melhor suporte")
    
    return None

def generate_music_ai(prompt, duration=30, output_path="output/music", model_key="musicgen-small"):
    """Gera música usando o modelo especificado"""
    
    models_config = load_models_config()
    
    if model_key not in models_config['music_models']:
        print(f"❌ Modelo '{model_key}' não encontrado!")
        print(f"💡 Use: python list_models.py para ver modelos disponíveis")
        return None
    
    model_info = models_config['music_models'][model_key]
    model_id = model_info['model_id']
    
    print(f"\n{'='*60}")
    print(f"🎵 Gerando Música com IA")
    print(f"{'='*60}")
    print(f"Modelo: {model_info['name']}")
    print(f"Qualidade: {model_info['quality']}")
    print(f"Tamanho: {model_info['size']}")
    print(f"GPU: {'Requerida' if model_info['gpu_required'] else 'Opcional'}")
    print(f"{'='*60}\n")
    
    # Criar diretório de saída
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    # Selecionar gerador baseado no modelo
    try:
        if "musicgen" in model_key:
            return generate_with_musicgen(model_id, prompt, duration, output_path)
        elif "audioldm" in model_key:
            return generate_with_audioldm(model_id, prompt, duration, output_path)
        elif "riffusion" in model_key:
            return generate_with_riffusion(model_id, prompt, duration, output_path)
        else:
            print(f"❌ Gerador não implementado para {model_key}")
            return None
    except ImportError as e:
        print(f"❌ Erro: Bibliotecas necessárias não instaladas")
        print(f"💡 Execute: pip install -r requirements-full.txt")
        print(f"Erro: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro ao gerar música: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Gerar música com IA (múltiplos modelos)')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da música')
    parser.add_argument('--duration', type=int, default=30, help='Duração em segundos')
    parser.add_argument('--output', type=str, default='output/music', help='Caminho de saída')
    parser.add_argument('--model', type=str, default='musicgen-small', help='Modelo a usar (veja list_models.py)')
    
    args = parser.parse_args()
    
    result = generate_music_ai(args.prompt, args.duration, args.output, args.model)
    
    if result:
        print(f"\n✅ Música gerada com sucesso: {result}")
    else:
        print(f"\n❌ Falha ao gerar música")

if __name__ == "__main__":
    main()
