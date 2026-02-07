#!/usr/bin/env python3
"""
Gerador de imagens usando Stable Diffusion
"""

import argparse
import os
import yaml
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def generate_image(prompt, output_path="output/cover.png"):
    """Gera imagem de capa baseada no prompt"""
    config = load_config()
    
    print(f"🎨 Carregando modelo Stable Diffusion...")
    
    # Verificar se há GPU disponível
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"📱 Usando dispositivo: {device}")
    
    # Carregar pipeline
    pipe = StableDiffusionPipeline.from_pretrained(
        config['image']['model'],
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)
    
    # Otimizações para economizar memória
    if device == "cuda":
        pipe.enable_attention_slicing()
    
    print(f"🖼️  Gerando imagem: '{prompt}'...")
    
    # Melhorar o prompt para capas de música
    enhanced_prompt = f"{prompt}, album cover art, professional design, high quality, detailed, artistic"
    
    # Gerar imagem
    image = pipe(
        enhanced_prompt,
        num_inference_steps=config['image']['steps'],
        width=config['image']['width'],
        height=config['image']['height']
    ).images[0]
    
    # Criar diretório de saída
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Salvar imagem
    print(f"💾 Salvando imagem em {output_path}...")
    image.save(output_path)
    
    print(f"✅ Imagem gerada com sucesso!")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Gerar imagem de capa com IA')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da imagem')
    parser.add_argument('--output', type=str, default='output/cover.png', help='Caminho de saída')
    
    args = parser.parse_args()
    
    generate_image(args.prompt, args.output)

if __name__ == "__main__":
    main()
