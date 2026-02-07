# 🎵 AI Music Generator for YouTube

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

Complete open-source project to generate music with AI, create professional artistic covers, and automatically upload to YouTube. 100% free!

## ✨ Features

- 🎼 **Multiple Music Models**: MusicGen, AudioLDM, Riffusion - choose the best for you
- 🎨 **High Quality Images**: Stable Diffusion with optimized prompts for lofi/anime style
- 🎯 **Smart Presets**: Quick, Balanced, Quality, Experimental
- 🎬 **Video Creation**: Automatically combines music + image
- 📤 **Automatic Upload**: Publish directly to YouTube with one command
- ⚙️ **Fully Configurable**: Choose models, quality and parameters
- 💰 **100% Free**: All tools are open-source
- 🖥️ **Works on CPU**: Optimized models to run without GPU (slower)

## 🚀 Quick Start

### Option 1: Quick Test (Without AI)

To quickly test the system without installing heavy models:

```bash
# Clone the repository
git clone https://github.com/uesleisutil/ai-music-generator.git
cd ai-music-generator

# Install basic dependencies
pip install -r requirements.txt

# Install FFmpeg
brew install ffmpeg  # macOS
# sudo apt install ffmpeg  # Linux

# Test the system (generates basic images)
python aimusic simple --prompt "cozy lofi music" --duration 30 --skip-upload
```

⚠️ **Note**: Simple mode generates basic/abstract images. For professional quality, use AI mode below.

### Option 2: Professional Quality (With AI) ⭐ RECOMMENDED

To generate **professional quality** images and music like lofi YouTube channels:

```bash
# Install AI models (~10-15GB)
pip install -r requirements-full.txt

# Generate music with AI (professional quality!)
python aimusic ai --prompt "cozy lofi coffee shop music" --duration 60 --skip-upload
```

📖 **Complete AI Guide**: [docs/AI_SETUP.md](docs/AI_SETUP.md)

## 📋 Requirements

### Basic (Simple Mode)
- Python 3.9+
- FFmpeg
- 4GB RAM

### Recommended (AI Mode)
- Python 3.9+
- FFmpeg
- 16GB+ RAM
- NVIDIA GPU with 6GB+ VRAM (optional, but much faster)
- 20GB+ disk space

## 📖 How to Use

### View Available Models

```bash
# List all models (13 free options!)
python aimusic models

# Check installed models
python aimusic check
```

### Generate with AI (Recommended)

```bash
# Use balanced preset (best cost-benefit)
python aimusic ai \
  --prompt "rainy night city lofi beats" \
  --preset balanced \
  --duration 180 \
  --skip-upload

# Choose specific models
python aimusic ai \
  --prompt "cozy coffee shop jazz" \
  --music-model musicgen-medium \
  --image-model sd-2-1 \
  --duration 120 \
  --skip-upload

# Maximum quality
python aimusic ai \
  --prompt "peaceful forest ambience" \
  --preset quality \
  --duration 180 \
  --skip-upload
```

### Available Presets

- `--preset quick` - Fast, works on CPU (basic quality)
- `--preset balanced` - Balance quality/speed ⭐ **RECOMMENDED**
- `--preset quality` - Maximum quality (requires powerful GPU)
- `--preset experimental` - Alternative models with unique styles

### Upload to YouTube

```bash
# Remove --skip-upload and configure YouTube API
python aimusic ai --prompt "chill beats" --duration 180 --title "Chill Lofi Beats"
```

📖 **Configure YouTube**: [docs/SETUP.md](docs/SETUP.md)

## 🎯 Prompt Examples

### Cafe/Interior
```bash
python aimusic ai --prompt "cozy coffee shop with plants and warm lighting"
```

### Night City
```bash
python aimusic ai --prompt "rainy night city with neon lights and reflections"
```

### Bedroom/Study
```bash
python aimusic ai --prompt "bedroom with city view and desk setup lofi"
```

### Nature
```bash
python aimusic ai --prompt "peaceful forest with sunlight through trees"
```

## 📊 Comparison: Simple vs AI

| Feature | Simple Mode | AI Mode |
|---------|-------------|---------|
| Image Quality | ⭐⭐ Basic | ⭐⭐⭐⭐⭐ Professional |
| Music Quality | ⭐⭐ Synthetic | ⭐⭐⭐⭐⭐ Natural |
| Speed | ⚡⚡⚡ Seconds | ⚡ Minutes |
| Requires GPU | ❌ No | ⚠️ Recommended |
| Download | ❌ No | ✅ 10-15GB |
| Use Case | Quick tests | Production |

## 🐛 Troubleshooting

### Images look bad/abstract
You're using simple mode. Install AI models:
```bash
pip install -r requirements-full.txt
python aimusic ai --prompt "test" --duration 30 --skip-upload
```

### Error: "No module named 'torch'"
```bash
pip install -r requirements-full.txt
```

### Too slow
Normal on CPU. Options:
- Use `--preset quick` for smaller models
- Reduce `--duration` to 30-60 seconds
- Use NVIDIA GPU to accelerate 10x

### FFmpeg not found
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

## 📁 Project Structure

```
ai-music-generator/
├── aimusic                 # Main CLI
├── src/                    # Source code
│   ├── generators/         # Music and image generators
│   ├── utils/              # Utilities (video, upload)
│   └── pipeline*.py        # Pipelines
├── scripts/                # Helper scripts
├── docs/                   # Complete documentation
└── tests/                  # Tests
```

## 📚 Documentation

- 📖 [Quick Start](docs/QUICKSTART.md)
- 🤖 [AI Setup](docs/AI_SETUP.md) ⭐ **IMPORTANT**
- 🎨 [Models Guide](docs/MODELS.md)
- 🔧 [Detailed Installation](docs/SETUP.md)
- 📁 [Project Structure](docs/PROJECT_STRUCTURE.md)

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

## 📄 License

This project is under the MIT license. See [LICENSE](LICENSE) for more details.

## 🙏 Acknowledgments

- [MusicGen](https://github.com/facebookresearch/audiocraft) by Meta
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) by Stability AI
- [FFmpeg](https://ffmpeg.org/)
- [YouTube Data API](https://developers.google.com/youtube/v3)

## ⭐ Star History

If this project helped you, consider giving it a star! ⭐

## 📧 Contact

Have questions? Open an [issue](https://github.com/uesleisutil/ai-music-generator/issues)!

---

**Made with ❤️ and AI**

**Tip**: For professional quality, always use `python aimusic ai` (not `simple`)!
