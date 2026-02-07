#!/usr/bin/env python3
"""
Lists all available models
"""

import yaml
from tabulate import tabulate


def load_models_config():
    with open('models_config.yaml', 'r') as f:
        return yaml.safe_load(f)


def list_music_models():
    """Lista models de music"""
    config = load_models_config()

    print("\n🎵 AVAILABLE MUSIC MODELS\n")

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

    headers = ["ID", "Name", "Quality", "Speed", "Size", "GPU", "Description"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def list_image_models():
    """Lista models de image"""
    config = load_models_config()

    print("\n🎨 AVAILABLE IMAGE MODELS\n")

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

    headers = ["ID", "Name", "Quality", "Speed", "Size", "GPU", "Description"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def list_presets():
    """Lista presets disponíveis"""
    config = load_models_config()

    print("\n⚙️  AVAILABLE PRESETS\n")

    table_data = []
    for key, preset in config['presets'].items():
        table_data.append([
            key,
            preset['music'],
            preset['image'],
            preset['description']
        ])

    headers = ["Preset", "Music Model", "Image Model", "Description"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    print("\n💡 Use: --preset quick|balanced|quality|experimental")


def main():
    print("=" * 80)
    print("🤖 AVAILABLE AI MODELS - 100% FREE")
    print("=" * 80)

    list_music_models()
    list_image_models()
    list_presets()

    print("\n" + "=" * 80)
    print("📖 HOW TO USE")
    print("=" * 80)
    print("\n# Usar model específico:")
    print("python pipeline.py --music-model musicgen-medium --image-model sd-2-1 --prompt 'test'")
    print("\n# Use preset:")
    print("python pipeline.py --preset balanced --prompt 'cozy lofi music'")
    print("\n# Listar models instalados:")
    print("python check_models.py")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
