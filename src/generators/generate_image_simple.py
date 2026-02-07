#!/usr/bin/env python3
"""
Gerador de imagem estilo lofi/chill com cenários detalhados
(Versão sem IA para testes rápidos)
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math


def create_lofi_cityscape(width, height, colors, accent_color):
    """Cria uma paisagem urbana estilo lofi com perspectiva"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Céu com gradiente (topo mais escuro)
    for y in range(int(height * 0.6)):
        ratio = y / (height * 0.6)
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))

    # Chão/rua (parte inferior)
    for y in range(int(height * 0.6), height):
        ratio = (y - height * 0.6) / (height * 0.4)
        r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * ratio)
        g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * ratio)
        b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))

    # Adicionar prédios com perspectiva
    img = img.convert('RGBA')
    buildings = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    buildings_draw = ImageDraw.Draw(buildings)

    # Prédios de fundo (menores, mais ao longe)
    horizon = int(height * 0.5)
    for i in range(20):
        x = random.randint(-50, width)
        building_width = random.randint(40, 100)
        building_height = random.randint(80, 200)
        y = horizon - building_height

        # Cor do prédio (escuro)
        darkness = random.randint(10, 40)
        buildings_draw.rectangle(
            [x, y, x + building_width, horizon],
            fill=(darkness, darkness, darkness + 10, 200)
        )

        # Janelas iluminadas (pequenas)
        for row in range(5, building_height - 10, 15):
            for col in range(5, building_width - 5, 12):
                if random.random() > 0.3:  # 70% das janelas acesas
                    window_color = random.choice([
                        accent_color,
                        (255, 220, 150),  # Amarelo quente
                        (150, 200, 255),  # Azul frio
                    ])
                    buildings_draw.rectangle(
                        [x + col, y + row, x + col + 6, y + row + 8],
                        fill=(*window_color, 220)
                    )

    # Prédios do meio (médios)
    for i in range(12):
        x = random.randint(-100, width)
        building_width = random.randint(80, 150)
        building_height = random.randint(150, 350)
        y = horizon - building_height + 50

        darkness = random.randint(15, 50)
        buildings_draw.rectangle(
            [x, y, x + building_width, horizon + 50],
            fill=(darkness, darkness, darkness + 15, 220)
        )

        # Janelas maiores
        for row in range(10, building_height - 15, 20):
            for col in range(8, building_width - 8, 15):
                if random.random() > 0.25:
                    window_color = random.choice([
                        accent_color,
                        (255, 200, 100),
                        (100, 180, 255),
                        (255, 150, 200),
                    ])
                    buildings_draw.rectangle(
                        [x + col, y + row, x + col + 8, y + row + 12],
                        fill=(*window_color, 240)
                    )

    # Prédios da frente (maiores, mais detalhados)
    for i in range(6):
        x = random.randint(-150, width - 100)
        building_width = random.randint(120, 250)
        building_height = random.randint(250, 500)
        y = horizon - building_height + 100

        darkness = random.randint(20, 60)
        buildings_draw.rectangle(
            [x, y, x + building_width, height],
            fill=(darkness, darkness, darkness + 20, 240)
        )

        # Janelas grandes e detalhadas
        for row in range(15, building_height - 20, 25):
            for col in range(12, building_width - 12, 20):
                if random.random() > 0.2:
                    window_color = random.choice([
                        accent_color,
                        (255, 220, 120),
                        (120, 200, 255),
                        (255, 180, 220),
                    ])
                    # Janela com brilho
                    buildings_draw.rectangle(
                        [x + col, y + row, x + col + 12, y + row + 16],
                        fill=(*window_color, 255)
                    )

    img = Image.alpha_composite(img, buildings)

    return img


def create_lofi_cafe(width, height, colors, accent_color):
    """Cria interior de café estilo lofi"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Fundo com gradiente quente
    for y in range(height):
        ratio = y / height
        r = int(colors[0][0] + (colors[2][0] - colors[0][0]) * ratio)
        g = int(colors[0][1] + (colors[2][1] - colors[0][1]) * ratio)
        b = int(colors[0][2] + (colors[2][2] - colors[0][2]) * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))

    img = img.convert('RGBA')
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Janelas grandes (luz entrando)
    window_light = (255, 240, 200, 100)
    overlay_draw.rectangle([50, 50, 400, 400], fill=window_light)
    overlay_draw.rectangle([width - 400, 50, width - 50, 400], fill=window_light)

    # Plantas (formas verdes)
    for i in range(15):
        x = random.randint(0, width)
        y = random.randint(int(height * 0.3), height)
        size = random.randint(30, 100)
        green = (random.randint(50, 100), random.randint(120, 180), random.randint(50, 100), 180)
        overlay_draw.ellipse([x, y, x + size, y + size], fill=green)

    # Mesas e cadeiras (retângulos marrons)
    for i in range(8):
        x = random.randint(100, width - 200)
        y = random.randint(int(height * 0.5), height - 100)
        table_color = (random.randint(80, 120), random.randint(50, 80), random.randint(30, 50), 200)
        overlay_draw.rectangle([x, y, x + 120, y + 80], fill=table_color)

    # Luzes quentes (círculos amarelos)
    for i in range(10):
        x = random.randint(0, width)
        y = random.randint(0, int(height * 0.4))
        size = random.randint(20, 60)
        overlay_draw.ellipse([x, y, x + size, y + size], fill=(255, 220, 150, 120))

    img = Image.alpha_composite(img, overlay)

    return img


def add_atmospheric_effects(img, accent_color):
    """Adiciona efeitos atmosféricos (névoa, brilho, partículas)"""
    width, height = img.size
    img = img.convert('RGBA')

    # Camada de névoa/atmosfera
    atmosphere = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    atm_draw = ImageDraw.Draw(atmosphere)

    # Névoa suave
    for i in range(8):
        x = random.randint(-200, width)
        y = random.randint(0, height)
        size = random.randint(300, 600)
        atm_draw.ellipse([x, y, x + size, y + size], fill=(*accent_color, 15))

    # Partículas flutuantes (poeira, neve, etc)
    for i in range(150):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 4)
        alpha = random.randint(50, 200)
        atm_draw.ellipse([x, y, x + size, y + size], fill=(255, 255, 255, alpha))

    # Brilhos de luz (lens flare effect)
    for i in range(5):
        x = random.randint(0, width)
        y = random.randint(0, int(height * 0.5))
        for radius in range(80, 10, -10):
            alpha = int(30 * (radius / 80))
            atm_draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=(255, 255, 200, alpha)
            )

    img = Image.alpha_composite(img, atmosphere)

    # Aplicar blur suave para efeito dreamy
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

    return img


def generate_simple_image(prompt, output_path="output/cover.png"):
    """
    Gera imagem estilo lofi/chill com cenários artísticos detalhados
    """
    print(f"⚠️  Usando gerador simples (sem IA)")
    print(f"🎨 Gerando imagem estilo lofi: '{prompt}'...")

    width, height = 1280, 720

    # Escolher paleta e estilo baseado no prompt
    prompt_lower = prompt.lower()

    if "coffee" in prompt_lower or "cafe" in prompt_lower:
        colors = [(80, 60, 40), (120, 90, 60), (160, 130, 90)]
        accent_color = (100, 180, 100)
        text_color = (255, 240, 220)
        scene_type = "cafe"
    elif "rain" in prompt_lower or "rainy" in prompt_lower:
        colors = [(20, 30, 50), (40, 60, 90), (60, 90, 130)]
        accent_color = (100, 150, 255)
        text_color = (200, 220, 255)
        scene_type = "city"
    elif "night" in prompt_lower or "city" in prompt_lower:
        colors = [(15, 20, 40), (40, 30, 80), (80, 50, 120)]
        accent_color = (255, 50, 150)
        text_color = (255, 150, 200)
        scene_type = "city"
    else:  # lofi padrão
        colors = [(30, 20, 60), (80, 50, 120), (150, 80, 180)]
        accent_color = (255, 100, 200)
        text_color = (255, 200, 255)
        scene_type = "city"

    # Criar cenário baseado no tipo
    if scene_type == "cafe":
        img = create_lofi_cafe(width, height, colors, accent_color)
    else:
        img = create_lofi_cityscape(width, height, colors, accent_color)

    # Adicionar efeitos atmosféricos
    img = add_atmospheric_effects(img, accent_color)

    # Converter para RGB para adicionar texto
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # Adicionar texto estilo lofi
    try:
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
        ]
        font_large = None
        font_small = None
        for font_path in font_paths:
            try:
                font_large = ImageFont.truetype(font_path, 65)
                font_small = ImageFont.truetype(font_path, 32)
                break
            except BaseException:
                continue
        if not font_large:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    except BaseException:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Processar título
    title = prompt.title()
    if len(title) > 35:
        title = title[:32] + "..."

    # Posicionar texto no terço inferior
    bbox = draw.textbbox((0, 0), title, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    text_y = int(height * 0.70)

    # Fundo semi-transparente para o texto
    img = img.convert('RGBA')
    text_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    text_bg_draw = ImageDraw.Draw(text_bg)

    padding = 40
    text_bg_draw.rectangle([
        text_x - padding,
        text_y - padding,
        text_x + text_width + padding,
        text_y + 110 + padding
    ], fill=(0, 0, 0, 140))

    img = Image.alpha_composite(img, text_bg).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Sombra do texto (múltiplas camadas para efeito mais forte)
    for offset in [(3, 3), (4, 4), (5, 5)]:
        draw.text((text_x + offset[0], text_y + offset[1]), title,
                  fill=(0, 0, 0), font=font_large)

    # Texto principal
    draw.text((text_x, text_y), title, fill=text_color, font=font_large)

    # Subtítulo
    subtitle = "🎵 AI Generated Lofi Music"
    bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    text_y = int(height * 0.70) + 75

    draw.text((text_x + 2, text_y + 2), subtitle, fill=(0, 0, 0), font=font_small)
    draw.text((text_x, text_y), subtitle, fill=(220, 220, 220), font=font_small)

    # Salvar
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"💾 Salvando imagem em {output_path}...")
    img.save(output_path, quality=95)

    print(f"✅ Imagem estilo lofi gerada!")
    print(f"💡 Para imagens reais com IA, instale: pip install diffusers torch")

    return output_path


def main():
    parser = argparse.ArgumentParser(description='Gerar imagem estilo lofi')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da imagem')
    parser.add_argument('--output', type=str, default='output/cover.png', help='Caminho de saída')

    args = parser.parse_args()

    generate_simple_image(args.prompt, args.output)


if __name__ == "__main__":
    main()
