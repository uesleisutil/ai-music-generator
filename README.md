# 🎵 AI Music Generator for YouTube

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

Projeto open-source completo para gerar músicas com IA, criar capas artísticas profissionais e fazer upload automático no YouTube. 100% gratuito!

## ✨ Features

- 🎼 **Múltiplos Modelos de Música**: MusicGen, AudioLDM, Riffusion - escolha o melhor para você
- 🎨 **Imagens de Alta Qualidade**: Stable Diffusion com prompts otimizados para estilo lofi/anime
- 🎯 **Presets Inteligentes**: Quick, Balanced, Quality, Experimental
- 🎬 **Criação de Vídeo**: Combina música + imagem automaticamente
- 📤 **Upload Automático**: Publica direto no YouTube com um comando
- ⚙️ **Totalmente Configurável**: Escolha modelos, qualidade e parâmetros
- 💰 **100% Gratuito**: Todas as ferramentas são open-source
- 🖥️ **Funciona em CPU**: Modelos otimizados para rodar sem GPU (mais lento)

## 🚀 Quick Start

### Opção 1: Teste Rápido (Sem IA)

Para testar o sistema rapidamente sem instalar modelos pesados:

```bash
# Clone o repositório
git clone https://github.com/uesleisutil/ai-music-generator.git
cd ai-music-generator

# Instale dependências básicas
pip install -r requirements.txt

# Instale FFmpeg
brew install ffmpeg  # macOS
# sudo apt install ffmpeg  # Linux

# Teste o sistema (gera imagens básicas)
python aimusic simple --prompt "cozy lofi music" --duration 30 --skip-upload
```

⚠️ **Nota**: O modo simples gera imagens básicas/abstratas. Para qualidade profissional, use o modo IA abaixo.

### Opção 2: Qualidade Profissional (Com IA) ⭐ RECOMENDADO

Para gerar imagens e músicas de **qualidade profissional** como canais lofi do YouTube:

```bash
# Instalar modelos de IA (~10-15GB)
pip install -r requirements-full.txt

# Gerar música com IA (qualidade profissional!)
python aimusic ai --prompt "cozy lofi coffee shop music" --duration 60 --skip-upload
```

📖 **Guia completo de IA**: [docs/AI_SETUP.md](docs/AI_SETUP.md)

## 📋 Requisitos

### Básico (Modo Simples)
- Python 3.9+
- FFmpeg
- 4GB RAM

### Recomendado (Modo IA)
- Python 3.9+
- FFmpeg
- 16GB+ RAM
- GPU NVIDIA com 6GB+ VRAM (opcional, mas acelera muito)
- 20GB+ espaço em disco

## 📖 Como Usar

### Ver Modelos Disponíveis

```bash
# Listar todos os modelos (13 opções gratuitas!)
python aimusic models

# Verificar modelos instalados
python aimusic check
```

### Gerar com IA (Recomendado)

```bash
# Usar preset balanced (melhor custo-benefício)
python aimusic ai \
  --prompt "rainy night city lofi beats" \
  --preset balanced \
  --duration 180 \
  --skip-upload

# Escolher modelos específicos
python aimusic ai \
  --prompt "cozy coffee shop jazz" \
  --music-model musicgen-medium \
  --image-model sd-2-1 \
  --duration 120 \
  --skip-upload

# Máxima qualidade
python aimusic ai \
  --prompt "peaceful forest ambience" \
  --preset quality \
  --duration 180 \
  --skip-upload
```

### Presets Disponíveis

- `--preset quick` - Rápido, funciona em CPU (qualidade básica)
- `--preset balanced` - Equilíbrio qualidade/velocidade ⭐ **RECOMENDADO**
- `--preset quality` - Máxima qualidade (requer GPU potente)
- `--preset experimental` - Modelos alternativos com estilos únicos

### Upload para YouTube

```bash
# Remova --skip-upload e configure YouTube API
python aimusic ai --prompt "chill beats" --duration 180 --title "Chill Lofi Beats"
```

📖 **Configurar YouTube**: [docs/SETUP.md](docs/SETUP.md)

## 🎯 Exemplos de Prompts

### Café/Interior
```bash
python aimusic ai --prompt "cozy coffee shop with plants and warm lighting"
```

### Cidade Noturna
```bash
python aimusic ai --prompt "rainy night city with neon lights and reflections"
```

### Quarto/Estudo
```bash
python aimusic ai --prompt "bedroom with city view and desk setup lofi"
```

### Natureza
```bash
python aimusic ai --prompt "peaceful forest with sunlight through trees"
```

## 📊 Comparação: Simples vs IA

| Feature | Modo Simples | Modo IA |
|---------|-------------|---------|
| Qualidade Imagem | ⭐⭐ Básica | ⭐⭐⭐⭐⭐ Profissional |
| Qualidade Música | ⭐⭐ Sintética | ⭐⭐⭐⭐⭐ Natural |
| Velocidade | ⚡⚡⚡ Segundos | ⚡ Minutos |
| Requer GPU | ❌ Não | ⚠️ Recomendado |
| Download | ❌ Não | ✅ 10-15GB |
| Uso | Testes rápidos | Produção |

## 🐛 Troubleshooting

### Imagens ficam ruins/abstratas
Você está usando o modo simples. Instale os modelos de IA:
```bash
pip install -r requirements-full.txt
python aimusic ai --prompt "test" --duration 30 --skip-upload
```

### Erro: "No module named 'torch'"
```bash
pip install -r requirements-full.txt
```

### Muito lento
Normal em CPU. Opções:
- Use `--preset quick` para modelos menores
- Reduza `--duration` para 30-60 segundos
- Use GPU NVIDIA para acelerar 10x

### FFmpeg não encontrado
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

## 📁 Estrutura do Projeto

```
ai-music-generator/
├── aimusic                 # CLI principal
├── src/                    # Código fonte
│   ├── generators/         # Geradores de música e imagem
│   ├── utils/              # Utilitários (vídeo, upload)
│   └── pipeline*.py        # Pipelines
├── scripts/                # Scripts auxiliares
├── docs/                   # Documentação completa
└── tests/                  # Testes
```

## 📚 Documentação

- 📖 [Guia Rápido](docs/QUICKSTART.md)
- 🤖 [Configuração de IA](docs/AI_SETUP.md) ⭐ **IMPORTANTE**
- 🎨 [Guia de Modelos](docs/MODELS.md)
- 🔧 [Instalação Detalhada](docs/SETUP.md)
- 📁 [Estrutura do Projeto](docs/PROJECT_STRUCTURE.md)

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](docs/CONTRIBUTING.md) para detalhes.

## � Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [MusicGen](https://github.com/facebookresearch/audiocraft) by Meta
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) by Stability AI
- [FFmpeg](https://ffmpeg.org/)
- [YouTube Data API](https://developers.google.com/youtube/v3)

## ⭐ Star History

Se este projeto te ajudou, considere dar uma estrela! ⭐

## 📧 Contato

Tem dúvidas? Abra uma [issue](https://github.com/uesleisutil/ai-music-generator/issues)!

---

**Feito com ❤️ e IA**

**Dica**: Para qualidade profissional, sempre use `python aimusic ai` (não `simple`)!
