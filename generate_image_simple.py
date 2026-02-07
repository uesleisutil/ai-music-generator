#!/usr/bin/env python3
"""
Gerador de imagem simples
(Versão sem IA para testes rápidos)
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import random

def generate_simple_image(prompt, output_path="output/cover.png"):
    """
    Gera imagem simples com gradiente e texto
    NOTA: Esta é uma versão simplificada para testes.
    Para imagens reais com IA, instale diffusers: pip install diffusers torch
    """
    print(f"⚠️  Usando gerador simples (sem IA)")
    print(f"🎨 Gerando imagem de teste: '{prompt}'...")
    
    # Dimensões
    width, height = 1280, 720
    
    # Escolher cores baseadas no prompt
    if "lofi" in prompt.lower() or "chill" in prompt.lower():
        colors = [(255, 182, 193), (176, 224, 230), (221, 160, 221)]  # Rosa, azul claro, lavanda
    elif "energetic" in prompt.lower() or "rock" in prompt.lower():
        colors = [(255, 69, 0), (255, 140, 0), (255, 215, 0)]  # Laranja, vermelho
    elif "jazz" in prompt.lower():
        colors = [(25, 25, 112), (72, 61, 139), (123, 104, 238)]  # Azul escuro, roxo
    else:
        colors = [(135, 206, 235), (176, 224, 230), (173, 216, 230)]  # Azul céu
    
    # Criar imagem com gradiente
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Gradiente vertical
    for y in range(height):
        ratio = y / height
        if ratio < 0.5:
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio * 2)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio * 2)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio * 2)
        else:
            r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * (ratio - 0.5) * 2)
            g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * (ratio - 0.5) * 2)
            b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * (ratio - 0.5) * 2)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    # Adicionar formas decorativas
    for _ in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(20, 100)
        color = random.choice(colors)
        alpha = random.randint(30, 80)
        
        # Criar círculo semi-transparente
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse([x, y, x + size, y + size], 
                            fill=(*color, alpha))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Adicionar texto
    draw = ImageDraw.Draw(img)
    
    # Tentar usar fonte do sistema
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Título
    title = prompt.upper()
    bbox = draw.textbbox((0, 0), title, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    text_y = height // 2 - 50
    
    # Sombra do texto
    draw.text((text_x + 3, text_y + 3), title, fill=(0, 0, 0, 128), font=font_large)
    # Texto principal
    draw.text((text_x, text_y), title, fill=(255, 255, 255), font=font_large)
    
    # Subtítulo
    subtitle = "AI Generated Music"
    bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    text_y = height // 2 + 50
    draw.text((text_x, text_y), subtitle, fill=(255, 255, 255, 200), font=font_small)
    
    # Criar diretório de saída
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Salvar imagem
    print(f"💾 Salvando imagem em {output_path}...")
    img.save(output_path, quality=95)
    
    print(f"✅ Imagem de teste gerada!")
    print(f"💡 Para imagens reais com IA, instale: pip install diffusers torch")
    
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Gerar imagem simples (sem IA)')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da imagem')
    parser.add_argument('--output', type=str, default='output/cover.png', help='Caminho de saída')
    
    args = parser.parse_args()
    
    generate_simple_image(args.prompt, args.output)

if __name__ == "__main__":
    main()
