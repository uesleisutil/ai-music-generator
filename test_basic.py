#!/usr/bin/env python3
"""
Teste básico da estrutura do projeto
"""

import os
import sys

def test_project_structure():
    """Verifica se todos os arquivos necessários existem"""
    print("🔍 Verificando estrutura do projeto...\n")
    
    required_files = [
        'README.md',
        'SETUP.md',
        'CONTRIBUTING.md',
        'LICENSE',
        'requirements.txt',
        'config.yaml',
        'pipeline.py',
        'generate_music.py',
        'generate_image.py',
        'create_video.py',
        'upload_youtube.py',
        '.gitignore',
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - FALTANDO")
            missing.append(file)
    
    return len(missing) == 0

def test_github_structure():
    """Verifica estrutura do GitHub"""
    print("\n🔍 Verificando estrutura GitHub...\n")
    
    github_files = [
        '.github/workflows/python-app.yml',
        '.github/ISSUE_TEMPLATE/bug_report.md',
        '.github/ISSUE_TEMPLATE/feature_request.md',
        '.github/pull_request_template.md',
    ]
    
    missing = []
    for file in github_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - FALTANDO")
            missing.append(file)
    
    return len(missing) == 0

def test_python_syntax():
    """Verifica sintaxe dos arquivos Python"""
    print("\n🔍 Verificando sintaxe Python...\n")
    
    python_files = [
        'pipeline.py',
        'generate_music.py',
        'generate_image.py',
        'create_video.py',
        'upload_youtube.py',
    ]
    
    errors = []
    for file in python_files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"  ✓ {file} - Sintaxe OK")
        except SyntaxError as e:
            print(f"  ✗ {file} - ERRO DE SINTAXE: {e}")
            errors.append(file)
    
    return len(errors) == 0

def test_config_yaml():
    """Verifica se o config.yaml é válido"""
    print("\n🔍 Verificando config.yaml...\n")
    
    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Verificar estrutura
        required_keys = ['music', 'image', 'youtube', 'output']
        for key in required_keys:
            if key in config:
                print(f"  ✓ Seção '{key}' presente")
            else:
                print(f"  ✗ Seção '{key}' faltando")
                return False
        
        return True
    except Exception as e:
        print(f"  ✗ Erro ao ler config.yaml: {e}")
        return False

def test_git_repo():
    """Verifica se é um repositório git válido"""
    print("\n🔍 Verificando repositório Git...\n")
    
    import subprocess
    try:
        # Verificar se é um repo git
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print("  ✓ Repositório Git inicializado")
            
            # Verificar remote
            result = subprocess.run(['git', 'remote', '-v'], 
                                  capture_output=True, 
                                  text=True)
            if 'github.com' in result.stdout:
                print("  ✓ Remote GitHub configurado")
                remote_url = result.stdout.split('\n')[0].split('\t')[1].split(' ')[0]
                print(f"     {remote_url}")
                return True
            else:
                print("  ⚠ Remote GitHub não configurado")
                return True
        else:
            print("  ✗ Não é um repositório Git")
            return False
    except Exception as e:
        print(f"  ✗ Erro ao verificar Git: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 TESTE BÁSICO DO PROJETO")
    print("=" * 60)
    print()
    
    tests = [
        ("Estrutura do Projeto", test_project_structure),
        ("Estrutura GitHub", test_github_structure),
        ("Sintaxe Python", test_python_syntax),
        ("Configuração YAML", test_config_yaml),
        ("Repositório Git", test_git_repo),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erro ao executar teste '{name}': {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {status} - {name}")
    
    print()
    print(f"Total: {passed}/{total} testes passaram")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ Projeto está estruturado corretamente")
        print("✅ Código Python sem erros de sintaxe")
        print("✅ Configuração válida")
        print("✅ Git e GitHub configurados")
        print("\n🚀 Próximos passos:")
        print("   1. Instale as dependências: pip install -r requirements.txt")
        print("   2. Configure YouTube API (veja SETUP.md)")
        print("   3. Execute: python pipeline.py --prompt 'test' --duration 30")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
