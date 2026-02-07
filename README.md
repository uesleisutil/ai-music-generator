# 🎵 AI Music Generator for YouTube

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

Projeto open-source completo para gerar músicas com IA, criar capas artísticas e fazer upload automático no YouTube. 100% gratuito!

## ✨ Features

- 🎼 **Múltiplos Modelos de Música**: MusicGen, AudioLDM, Riffusion - escolha o melhor para você
- 🎨 **Múltiplos Modelos de Imagem**: Stable Diffusion (1.5, 2.1, XL), Kandinsky, Würstchen, DeepFloyd
- � **Presets Inteligentes**: Quick, Balanced, Quality, Eixperimental
- 🎬 **Criação de Vídeo**: Combina música + imagem automaticamente
- 📤 **Upload Automático**: Publica direto no YouTube com um comando
- ⚙️ **Totalmente Configurável**: Escolha modelos, qualidade e parâmetros
- 💰 **100% Gratuito**: Todas as ferramentas são open-source
- 🖥️ **Funciona em CPU**: Modelos otimizados para rodar sem GPU

## 🚀 Quick Start

### Teste Rápido (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/uesleisutil/ai-music-generator.git
cd ai-music-generator

# Instale dependências básicas
pip install -r requirements.txt

# Instale FFmpeg
brew install ffmpeg  # macOS
# sudo apt install ffmpeg  # Linux

# Teste o sistema (sem IA, rápido!)
python pipeline_simple.py --prompt "cozy lofi music" --duration 30 --title "Test" --skip-upload
```

✅ **Pronto!** Seus arquivos estarão em `output/`

### Modo Completo com IA

Para usar modelos de IA reais (requer GPU recomendada):

```bash
# Instalar modelos de IA (~10GB)
pip install -r requirements-full.txt

# Gerar música com IA
python pipeline.py --prompt "cozy lofi home music" --duration 180 --title "My AI Music"
```

📖 **Guia completo:** [QUICKSTART.md](QUICKSTART.md)

## 📋 Requisitos

- Python 3.9+
- FFmpeg
- 8GB+ RAM (16GB recomendado)
- GPU NVIDIA (opcional, mas acelera muito)
- Conta Google (para YouTube API)

## 🛠️ Instalação Detalhada

Veja o guia completo em [SETUP.md](SETUP.md)

## 📖 Como Usar

### Ver Modelos Disponíveis

```bash
# Listar todos os modelos
python list_models.py

# Verificar modelos instalados
python check_models.py
```

### Pipeline Completo com IA

```bash
# Usar preset (recomendado)
python pipeline_ai.py \
  --prompt "cozy lofi music" \
  --preset balanced \
  --duration 180 \
  --skip-upload

# Escolher modelos específicos
python pipeline_ai.py \
  --prompt "epic orchestral" \
  --music-model musicgen-large \
  --image-model sd-xl-base \
  --duration 120 \
  --skip-upload
```

### Presets Disponíveis

- `--preset quick` - Rápido, funciona em CPU
- `--preset balanced` - Equilíbrio qualidade/velocidade (requer GPU)
- `--preset quality` - Máxima qualidade (requer GPU potente)
- `--preset experimental` - Modelos alternativos com estilos únicos

### Uso Individual

```bash
# Apenas gerar música
python generate_music_ai.py --prompt "jazz piano" --model musicgen-medium --duration 60

# Apenas gerar imagem
python generate_image_ai.py --prompt "jazz album cover" --model sd-2-1

# Criar vídeo
python create_video.py --audio output/music.wav --image output/cover.png

# Upload para YouTube
python upload_youtube.py --video output/video.mp4 --title "My Music"
```

📖 **Guia completo de modelos:** [MODELS.md](MODELS.md)

## ⚙️ Configuração

Edite `config.yaml` para personalizar:

```yaml
music:
  model: "facebook/musicgen-small"  # small, medium, large
  duration: 30

image:
  model: "stabilityai/stable-diffusion-2-1"
  width: 1280
  height: 720
  steps: 30

youtube:
  privacy: "public"  # public, private, unlisted
```

## 📁 Estrutura do Projeto

```
ai-music-generator/
├── pipeline.py              # Script principal
├── generate_music.py        # Geração de música
├── generate_image.py        # Geração de imagens
├── create_video.py          # Criação de vídeo
├── upload_youtube.py        # Upload YouTube
├── config.yaml              # Configurações
├── requirements.txt         # Dependências Python
├── SETUP.md                 # Guia de instalação
├── CONTRIBUTING.md          # Guia de contribuição
├── LICENSE                  # Licença MIT
└── .gitignore              # Arquivos ignorados
```

## 🎯 Exemplos de Prompts

- `"cozy lofi home music with rain sounds"`
- `"epic cinematic orchestral trailer music"`
- `"upbeat electronic dance music"`
- `"calm acoustic guitar meditation"`
- `"energetic rock guitar solo"`
- `"smooth jazz saxophone evening"`

## 🐛 Troubleshooting

### Erro de memória
- Use `musicgen-small` no config.yaml
- Reduza a duração da música
- Feche outros programas

### FFmpeg não encontrado
```bash
# Verifique instalação
ffmpeg -version

# Reinstale se necessário
brew install ffmpeg  # macOS
```

### Erro de autenticação YouTube
- Verifique se `client_secrets.json` está correto
- Delete `token.pickle` e tente novamente
- Veja guia completo em SETUP.md

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📝 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [MusicGen](https://github.com/facebookresearch/audiocraft) by Meta
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) by Stability AI
- [FFmpeg](https://ffmpeg.org/)
- [YouTube Data API](https://developers.google.com/youtube/v3)

## ⭐ Star History

Se este projeto te ajudou, considere dar uma estrela! ⭐

## 📧 Contato

Tem dúvidas? Abra uma [issue](https://github.com/SEU_USUARIO/ai-music-generator/issues)!

---

**Feito com ❤️ e IA**
