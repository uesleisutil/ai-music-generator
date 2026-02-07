# 📁 Estrutura do Projeto

## Visão Geral

```
ai-music-generator/
├── aimusic                    # CLI principal
├── setup.py                   # Instalação do pacote
├── requirements.txt           # Dependências básicas
├── requirements-full.txt      # Dependências com IA
├── config.yaml               # Configurações gerais
├── models_config.yaml        # Configuração de modelos
├── README.md                 # Documentação principal
├── LICENSE                   # Licença MIT
│
├── src/                      # Código fonte principal
│   ├── __init__.py
│   ├── pipeline.py           # Pipeline original
│   ├── pipeline_simple.py    # Pipeline sem IA
│   ├── pipeline_ai.py        # Pipeline com IA
│   │
│   ├── generators/           # Geradores de música e imagem
│   │   ├── __init__.py
│   │   ├── generate_music.py
│   │   ├── generate_music_simple.py
│   │   ├── generate_music_ai.py
│   │   ├── generate_image.py
│   │   ├── generate_image_simple.py
│   │   └── generate_image_ai.py
│   │
│   └── utils/                # Utilitários
│       ├── __init__.py
│       ├── create_video.py
│       └── upload_youtube.py
│
├── scripts/                  # Scripts auxiliares
│   ├── __init__.py
│   ├── list_models.py        # Lista modelos disponíveis
│   ├── check_models.py       # Verifica modelos instalados
│   ├── test_basic.py         # Teste básico
│   └── test_setup.py         # Teste de configuração
│
├── tests/                    # Testes automatizados
│   ├── __init__.py
│   └── test_setup.py
│
├── docs/                     # Documentação
│   ├── QUICKSTART.md         # Guia rápido
│   ├── SETUP.md              # Guia de instalação
│   ├── MODELS.md             # Guia de modelos
│   ├── CONTRIBUTING.md       # Guia de contribuição
│   ├── CHANGELOG.md          # Histórico de versões
│   ├── CODE_OF_CONDUCT.md    # Código de conduta
│   ├── DEPLOY.md             # Guia de deploy
│   ├── STATUS.md             # Status do projeto
│   ├── SUMMARY.md            # Resumo do projeto
│   └── PROJECT_STRUCTURE.md  # Este arquivo
│
├── .github/                  # GitHub Actions e templates
│   ├── workflows/
│   │   └── python-app.yml    # CI/CD
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── pull_request_template.md
│   └── FUNDING.yml
│
└── output/                   # Arquivos gerados (gitignored)
    ├── music.wav
    ├── cover.png
    └── video.mp4
```

## 📦 Módulos Principais

### `src/`
Código fonte principal do projeto.

#### `src/pipeline*.py`
- **pipeline.py**: Pipeline original com MusicGen
- **pipeline_simple.py**: Pipeline rápido sem IA
- **pipeline_ai.py**: Pipeline completo com múltiplos modelos

#### `src/generators/`
Geradores de música e imagem.

- **generate_music_simple.py**: Síntese de áudio simples
- **generate_music_ai.py**: Geração com múltiplos modelos de IA
- **generate_image_simple.py**: Geração de gradientes
- **generate_image_ai.py**: Geração com múltiplos modelos de IA

#### `src/utils/`
Utilitários compartilhados.

- **create_video.py**: Combina áudio e imagem em vídeo
- **upload_youtube.py**: Upload automático para YouTube

### `scripts/`
Scripts auxiliares e ferramentas.

- **list_models.py**: Lista todos os modelos disponíveis
- **check_models.py**: Verifica modelos instalados
- **test_basic.py**: Teste de estrutura do projeto
- **test_setup.py**: Teste de configuração

### `tests/`
Testes automatizados (pytest).

### `docs/`
Documentação completa do projeto.

## 🚀 CLI - `aimusic`

Interface de linha de comando unificada.

### Comandos

```bash
# Geração rápida (sem IA)
aimusic simple --prompt "lofi music" --duration 30

# Geração com IA (preset)
aimusic ai --prompt "jazz piano" --preset balanced --duration 60

# Geração com IA (modelos específicos)
aimusic ai --prompt "rock" --music-model musicgen-large --image-model sd-xl-base

# Listar modelos
aimusic models

# Verificar instalados
aimusic check

# Testar sistema
aimusic test
```

## 📝 Arquivos de Configuração

### `config.yaml`
Configurações gerais do projeto (duração padrão, qualidade, etc).

### `models_config.yaml`
Configuração de todos os modelos disponíveis:
- Modelos de música (7 opções)
- Modelos de imagem (6 opções)
- Presets (4 configurações)

### `requirements.txt`
Dependências básicas (funciona sem IA).

### `requirements-full.txt`
Dependências completas incluindo modelos de IA.

### `.flake8`
Configuração do linter Python.

### `pytest.ini`
Configuração do pytest.

### `setup.py`
Configuração de instalação do pacote.

## 🔄 CI/CD

### `.github/workflows/python-app.yml`
Pipeline de CI/CD que:
- Testa em Python 3.9, 3.10, 3.11
- Executa linting com flake8
- Verifica estrutura do projeto
- Testa imports
- Valida CLI
- Verifica documentação

## 📤 Output

### `output/`
Diretório onde são salvos os arquivos gerados:
- `music.wav` - Áudio gerado
- `cover.png` - Imagem de capa
- `video.mp4` - Vídeo final

**Nota**: Este diretório está no `.gitignore`.

## 🔧 Desenvolvimento

### Adicionar Novo Gerador

1. Criar arquivo em `src/generators/`
2. Implementar função principal
3. Adicionar ao `__init__.py`
4. Atualizar `models_config.yaml`
5. Adicionar testes

### Adicionar Novo Modelo

1. Adicionar configuração em `models_config.yaml`
2. Implementar suporte no gerador apropriado
3. Atualizar documentação em `docs/MODELS.md`
4. Testar com `aimusic check`

### Executar Testes

```bash
# Teste básico
python scripts/test_basic.py

# Teste de configuração
python scripts/test_setup.py

# Todos os testes (pytest)
pytest
```

## 📚 Documentação

Toda documentação está em `docs/`:

- **QUICKSTART.md**: Início rápido
- **SETUP.md**: Instalação detalhada
- **MODELS.md**: Guia completo de modelos
- **CONTRIBUTING.md**: Como contribuir
- **PROJECT_STRUCTURE.md**: Este arquivo

## 🎯 Fluxo de Trabalho

1. Usuário executa `aimusic` com parâmetros
2. CLI valida argumentos e chama pipeline apropriado
3. Pipeline carrega configurações
4. Geradores criam música e imagem
5. Utilitário combina em vídeo
6. (Opcional) Upload para YouTube
7. Arquivos salvos em `output/`

## 🔐 Segurança

- Credenciais do YouTube (`client_secrets.json`) no `.gitignore`
- Tokens de autenticação (`token.pickle`) no `.gitignore`
- Cache de modelos (`~/.cache/huggingface/`) fora do projeto

## 📊 Métricas

- **Linhas de código**: ~2500+
- **Módulos**: 15+
- **Scripts**: 5
- **Testes**: 2
- **Documentação**: 10 arquivos
- **Modelos suportados**: 13

---

**Última atualização**: 2026-02-07  
**Versão**: 2.0.0
