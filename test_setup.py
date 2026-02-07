#!/usr/bin/env python3
"""
Script de teste para verificar se tudo está configurado corretamente
"""

import sys

def test_imports():
    """Testa se todos os módulos necessários estão instalados"""
    print("🔍 Testando imports...")
    
    tests = {
        'yaml': 'PyYAML',
        'torch': 'PyTorch',
        'PIL': 'Pillow',
    }
    
    optional_tests = {
        'audiocraft': 'AudioCraft (MusicGen)',
        'diffusers': 'Diffusers (Stable Diffusion)',
        'transformers': 'Transformers',
        'google.auth': 'Google Auth',
        'googleapiclient': 'Google API Client',
    }
    
    failed = []
    optional_failed = []
    
    # Testes obrigatórios
    for module, name in tests.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - FALTANDO")
            failed.append(name)
    
    # Testes opcionais
    for module, name in optional_tests.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ⚠ {name} - Não instalado (necessário para funcionalidade completa)")
            optional_failed.append(name)
    
    return failed, optional_failed

def test_ffmpeg():
    """Testa se FFmpeg está instalado"""
    print("\n🔍 Testando FFmpeg...")
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"  ✓ {version}")
            return True
        else:
            print("  ✗ FFmpeg não está funcionando corretamente")
            return False
    except FileNotFoundError:
        print("  ✗ FFmpeg não encontrado")
        print("     Instale com: brew install ffmpeg")
        return False
    except Exception as e:
        print(f"  ✗ Erro ao testar FFmpeg: {e}")
        return False

def test_config():
    """Testa se o arquivo de configuração existe e é válido"""
    print("\n🔍 Testando configuração...")
    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("  ✓ config.yaml encontrado e válido")
        print(f"     Modelo de música: {config['music']['model']}")
        print(f"     Modelo de imagem: {config['image']['model']}")
        return True
    except FileNotFoundError:
        print("  ✗ config.yaml não encontrado")
        return False
    except Exception as e:
        print(f"  ✗ Erro ao ler config.yaml: {e}")
        return False

def test_youtube_credentials():
    """Verifica se as credenciais do YouTube estão configuradas"""
    print("\n🔍 Testando credenciais YouTube...")
    import os
    if os.path.exists('client_secrets.json'):
        print("  ✓ client_secrets.json encontrado")
        return True
    else:
        print("  ⚠ client_secrets.json não encontrado")
        print("     Necessário apenas para upload no YouTube")
        print("     Veja SETUP.md para instruções")
        return False

def main():
    print("=" * 60)
    print("🧪 TESTE DE CONFIGURAÇÃO - AI Music Generator")
    print("=" * 60)
    
    failed, optional_failed = test_imports()
    ffmpeg_ok = test_ffmpeg()
    config_ok = test_config()
    youtube_ok = test_youtube_credentials()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO")
    print("=" * 60)
    
    if failed:
        print(f"\n❌ FALHOU - Módulos obrigatórios faltando:")
        for module in failed:
            print(f"   - {module}")
        print("\n💡 Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    if optional_failed:
        print(f"\n⚠️  Módulos opcionais faltando (necessários para funcionalidade completa):")
        for module in optional_failed:
            print(f"   - {module}")
        print("\n💡 Execute: pip install -r requirements.txt")
    
    if not ffmpeg_ok:
        print("\n⚠️  FFmpeg não está instalado")
        print("💡 Execute: brew install ffmpeg")
    
    if not config_ok:
        print("\n❌ Arquivo de configuração com problemas")
        sys.exit(1)
    
    if not youtube_ok:
        print("\n⚠️  Credenciais do YouTube não configuradas")
        print("   (Opcional - necessário apenas para upload)")
    
    if not failed and ffmpeg_ok and config_ok:
        print("\n✅ TUDO PRONTO! Você pode começar a usar o projeto.")
        print("\n🚀 Teste rápido:")
        print("   python pipeline.py --prompt 'cozy lofi music' --duration 30 --title 'Test'")
    else:
        print("\n⚠️  Configuração parcial - algumas funcionalidades podem não funcionar")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
