#!/usr/bin/env python3
"""
Verifica quais modelos estão instalados/disponíveis
"""

import os
import yaml
from pathlib import Path

def load_models_config():
    with open('models_config.yaml', 'r') as f:
        return yaml.safe_load(f)

def check_cache_dir():
    """Verifica diretório de cache do Hugging Face"""
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    if cache_dir.exists():
        return cache_dir
    return None

def check_model_installed(model_id):
    """Verifica se um modelo está no cache"""
    cache_dir = check_cache_dir()
    if not cache_dir:
        return False
    
    # Converter model_id para formato de diretório
    model_dir_name = "models--" + model_id.replace("/", "--")
    model_path = cache_dir / model_dir_name
    
    return model_path.exists()

def get_model_size(model_id):
    """Obtém tamanho do modelo no cache"""
    cache_dir = check_cache_dir()
    if not cache_dir:
        return 0
    
    model_dir_name = "models--" + model_id.replace("/", "--")
    model_path = cache_dir / model_dir_name
    
    if not model_path.exists():
        return 0
    
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(model_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    
    return total_size

def format_size(size_bytes):
    """Formata tamanho em bytes para formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def check_dependencies():
    """Verifica dependências instaladas"""
    print("\n🔍 VERIFICANDO DEPENDÊNCIAS\n")
    
    deps = {
        'torch': 'PyTorch',
        'transformers': 'Transformers',
        'diffusers': 'Diffusers',
        'audiocraft': 'AudioCraft',
        'scipy': 'SciPy',
        'PIL': 'Pillow',
    }
    
    installed = []
    missing = []
    
    for module, name in deps.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
            installed.append(name)
        except ImportError:
            print(f"  ✗ {name} - NÃO INSTALADO")
            missing.append(name)
    
    return installed, missing

def main():
    print("=" * 80)
    print("🔍 VERIFICAÇÃO DE MODELOS E DEPENDÊNCIAS")
    print("=" * 80)
    
    # Verificar dependências
    installed_deps, missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"\n⚠️  Dependências faltando: {', '.join(missing_deps)}")
        print("💡 Execute: pip install -r requirements-full.txt")
    
    # Verificar modelos
    config = load_models_config()
    
    print("\n" + "=" * 80)
    print("🎵 MODELOS DE MÚSICA")
    print("=" * 80)
    
    for key, model in config['music_models'].items():
        model_id = model['model_id']
        installed = check_model_installed(model_id)
        
        if installed:
            size = get_model_size(model_id)
            print(f"\n✓ {key}")
            print(f"  Nome: {model['name']}")
            print(f"  Status: INSTALADO")
            print(f"  Tamanho no disco: {format_size(size)}")
        else:
            print(f"\n✗ {key}")
            print(f"  Nome: {model['name']}")
            print(f"  Status: NÃO INSTALADO")
            print(f"  Tamanho estimado: {model['size']}")
    
    print("\n" + "=" * 80)
    print("🎨 MODELOS DE IMAGEM")
    print("=" * 80)
    
    for key, model in config['image_models'].items():
        model_id = model['model_id']
        installed = check_model_installed(model_id)
        
        if installed:
            size = get_model_size(model_id)
            print(f"\n✓ {key}")
            print(f"  Nome: {model['name']}")
            print(f"  Status: INSTALADO")
            print(f"  Tamanho no disco: {format_size(size)}")
        else:
            print(f"\n✗ {key}")
            print(f"  Nome: {model['name']}")
            print(f"  Status: NÃO INSTALADO")
            print(f"  Tamanho estimado: {model['size']}")
    
    # Resumo
    cache_dir = check_cache_dir()
    if cache_dir:
        total_size = sum(get_model_size(m['model_id']) 
                        for models in [config['music_models'], config['image_models']] 
                        for m in models.values())
        
        print("\n" + "=" * 80)
        print("📊 RESUMO")
        print("=" * 80)
        print(f"\nCache: {cache_dir}")
        print(f"Espaço usado: {format_size(total_size)}")
        print(f"\n💡 Os modelos são baixados automaticamente na primeira vez que você os usa")
        print(f"💡 Use: python list_models.py para ver todos os modelos disponíveis")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
