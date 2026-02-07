#!/usr/bin/env python3
"""
Lista todos os modelos disponíveis
"""

import yaml
from tabulate import tabulate


def load_models_config():
    with open('models_config.yaml', 'r') as f:
        return yaml.safe_load(f)


def list_music_models():
    """Lista modelos de música"""
    config = load_models_config()

    print("\n🎵 MODELOS DE MÚSICA DISPONÍVEIS\n")

    table_data = []
    for key, model in config['music_models'].items():
        gpu = "✓" if model['gpu_required'] else "✗"
        table_data.append([
            key,
            model['name'],
            model['quality'],
            model['speed'],
            model['size'],
            gpu,
            model['description']
        ])

    headers = ["ID", "Nome", "Qualidade", "Velocidade", "Tamanho", "GPU", "Descrição"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def list_image_models():
    """Lista modelos de imagem"""
    config = load_models_config()

    print("\n🎨 MODELOS DE IMAGEM DISPONÍVEIS\n")

    table_data = []
    for key, model in config['image_models'].items():
        gpu = "✓" if model['gpu_required'] else "✗"
        table_data.append([
            key,
            model['name'],
            model['quality'],
            model['speed'],
            model['size'],
            gpu,
            model['description']
        ])

    headers = ["ID", "Nome", "Qualidade", "Velocidade", "Tamanho", "GPU", "Descrição"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def list_presets():
    """Lista presets disponíveis"""
    config = load_models_config()

    print("\n⚙️  PRESETS DISPONÍVEIS\n")

    table_data = []
    for key, preset in config['presets'].items():
        table_data.append([
            key,
            preset['music'],
            preset['image'],
            preset['description']
        ])

    headers = ["Preset", "Modelo Música", "Modelo Imagem", "Descrição"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    print("\n💡 Use: --preset quick|balanced|quality|experimental")


def main():
    print("=" * 80)
    print("🤖 MODELOS DE IA DISPONÍVEIS - 100% GRATUITOS")
    print("=" * 80)

    list_music_models()
    list_image_models()
    list_presets()

    print("\n" + "=" * 80)
    print("📖 COMO USAR")
    print("=" * 80)
    print("\n# Usar modelo específico:")
    print("python pipeline.py --music-model musicgen-medium --image-model sd-2-1 --prompt 'test'")
    print("\n# Usar preset:")
    print("python pipeline.py --preset balanced --prompt 'cozy lofi music'")
    print("\n# Listar modelos instalados:")
    print("python check_models.py")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
