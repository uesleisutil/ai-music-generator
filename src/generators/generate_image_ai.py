#!/usr/bin/env python3
"""
Gerador de imagens usando múltiplos modelos de IA
"""

import argparse
import os
import yaml
import torch

def load_models_config():
    with open('models_config.yaml', 'r') as f:
        return yaml.safe_load(f)

def generate_with_stable_diffusion(model_id, prompt, output_path, width=1280, height=720):
    """Gera imagem usando Stable Diffusion"""
    from diffusers import StableDiffusionPipeline
    
    print(f"🎨 Carregando Stable Diffusion ({model_id})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)
    
    if device == "cuda":
        pipe.enable_attention_slicing()
    
    print(f"🖼️  Gerando imagem: '{prompt}'...")
    enhanced_prompt = f"{prompt}, album cover art, professional design, high quality, detailed, artistic"
    
    image = pipe(
        enhanced_prompt,
        num_inference_steps=30,
        width=width,
        height=height
    ).images[0]
    
    image.save(output_path)
    return output_path

def generate_with_sdxl(model_id, prompt, output_path, width=1280, height=720):
    """Gera imagem usando Stable Diffusion XL"""
    from diffusers import StableDiffusionXLPipeline
    
    print(f"🎨 Carregando SDXL ({model_id})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)
    
    print(f"🖼️  Gerando imagem: '{prompt}'...")
    enhanced_prompt = f"{prompt}, album cover art, professional design, high quality"
    
    image = pipe(
        enhanced_prompt,
        num_inference_steps=30,
        width=width,
        height=height
    ).images[0]
    
    image.save(output_path)
    return output_path

def generate_with_kandinsky(model_id, prompt, output_path, width=1280, height=720):
    """Gera imagem usando Kandinsky"""
    from diffusers import KandinskyV22Pipeline, KandinskyV22PriorPipeline
    
    print(f"🎨 Carregando Kandinsky ({model_id})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Kandinsky usa dois estágios
    prior = KandinskyV22PriorPipeline.from_pretrained(
        "kandinsky-community/kandinsky-2-2-prior",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)
    
    pipe = KandinskyV22Pipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)
    
    print(f"🖼️  Gerando imagem: '{prompt}'...")
    enhanced_prompt = f"{prompt}, album cover, artistic, detailed"
    
    image_embeds, negative_embeds = prior(enhanced_prompt).to_tuple()
    
    image = pipe(
        image_embeds=image_embeds,
        negative_image_embeds=negative_embeds,
        height=height,
        width=width
    ).images[0]
    
    image.save(output_path)
    return output_path

def generate_image_ai(prompt, output_path="output/cover.png", model_key="sd-1-5", width=1280, height=720):
    """Gera imagem usando o modelo especificado"""
    
    models_config = load_models_config()
    
    if model_key not in models_config['image_models']:
        print(f"❌ Modelo '{model_key}' não encontrado!")
        print(f"💡 Use: python list_models.py para ver modelos disponíveis")
        return None
    
    model_info = models_config['image_models'][model_key]
    model_id = model_info['model_id']
    
    print(f"\n{'='*60}")
    print(f"🎨 Gerando Imagem com IA")
    print(f"{'='*60}")
    print(f"Modelo: {model_info['name']}")
    print(f"Qualidade: {model_info['quality']}")
    print(f"Tamanho: {model_info['size']}")
    print(f"GPU: {'Requerida' if model_info['gpu_required'] else 'Opcional'}")
    print(f"{'='*60}\n")
    
    # Criar diretório de saída
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Selecionar gerador baseado no modelo
    try:
        if "sd-xl" in model_key:
            return generate_with_sdxl(model_id, prompt, output_path, width, height)
        elif "kandinsky" in model_key:
            return generate_with_kandinsky(model_id, prompt, output_path, width, height)
        elif "sd-" in model_key or "stable-diffusion" in model_key:
            return generate_with_stable_diffusion(model_id, prompt, output_path, width, height)
        else:
            # Fallback para Stable Diffusion padrão
            return generate_with_stable_diffusion(model_id, prompt, output_path, width, height)
    except ImportError as e:
        print(f"❌ Erro: Bibliotecas necessárias não instaladas")
        print(f"💡 Execute: pip install -r requirements-full.txt")
        print(f"Erro: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro ao gerar imagem: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Gerar imagem com IA (múltiplos modelos)')
    parser.add_argument('--prompt', type=str, required=True, help='Descrição da imagem')
    parser.add_argument('--output', type=str, default='output/cover.png', help='Caminho de saída')
    parser.add_argument('--model', type=str, default='sd-1-5', help='Modelo a usar (veja list_models.py)')
    parser.add_argument('--width', type=int, default=1280, help='Largura da imagem')
    parser.add_argument('--height', type=int, default=720, help='Altura da imagem')
    
    args = parser.parse_args()
    
    result = generate_image_ai(args.prompt, args.output, args.model, args.width, args.height)
    
    if result:
        print(f"\n✅ Imagem gerada com sucesso: {result}")
    else:
        print(f"\n❌ Falha ao gerar imagem")

if __name__ == "__main__":
    main()
