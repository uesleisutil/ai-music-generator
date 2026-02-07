# 🤖 AI Setup - Complete Guide

## Why use AI models?

The simple generator (without AI) creates basic images with geometric shapes. To get **professional quality** images like lofi YouTube channel examples, you **need** to install AI models.

## 📦 Quick Installation

```bash
# Install all AI dependencies
pip install -r requirements-full.txt
```

⚠️ **Warning**: This will download ~10-15GB of models. Make sure you have:
- Disk space: 20GB+ free
- RAM: 16GB recommended
- GPU: NVIDIA with 6GB+ VRAM (recommended, but works on CPU)

## 🎨 Recommended Models

### For Best Quality (Default)

**Music**: `musicgen-medium`
- Size: 1.5GB
- Quality: Good
- Speed: Medium
- GPU: Recommended

**Image**: `sd-2-1` (Stable Diffusion 2.1)
- Size: 5GB
- Quality: Excellent
- Speed: Medium
- GPU: Recommended

### For Maximum Quality

```bash
python aimusic ai \
  --prompt "cozy lofi coffee shop" \
  --preset quality \
  --duration 180
```

Uses:
- `musicgen-large` (3.3GB)
- `sd-xl-base` (7GB)

### For Quick Tests

```bash
python aimusic ai \
  --prompt "lofi beats" \
  --preset quick \
  --duration 30
```

Uses:
- `musicgen-small` (300MB)
- `wuerstchen` (3GB)

## 🚀 Using with AI

### Basic Command

```bash
# Use default models (recommended)
python aimusic ai --prompt "rainy night city lofi" --duration 60 --skip-upload
```

### Choose Specific Models

```bash
# Music: medium, Image: SD 2.1
python aimusic ai \
  --prompt "cozy coffee shop music" \
  --music-model musicgen-medium \
  --image-model sd-2-1 \
  --duration 120 \
  --skip-upload
```

### Use Presets

```bash
# Balanced preset (best cost-benefit)
python aimusic ai --prompt "chill beats" --preset balanced --duration 180

# Quality preset (maximum quality)
python aimusic ai --prompt "jazz lofi" --preset quality --duration 180

# Quick preset (quick tests)
python aimusic ai --prompt "test" --preset quick --duration 30
```

## 📊 Comparison: Simple vs AI

### Simple Mode (without AI)
```bash
python aimusic simple --prompt "lofi music" --duration 30
```
- ✅ Fast (seconds)
- ✅ No GPU needed
- ✅ No download needed
- ❌ Basic quality
- ❌ Abstract/geometric images
- ❌ Simple synthetic music

### AI Mode
```bash
python aimusic ai --prompt "lofi music" --duration 30
```
- ✅ Professional quality
- ✅ Realistic/artistic images
- ✅ Complex and natural music
- ⚠️ Requires model download
- ⚠️ Slower (minutes)
- ⚠️ GPU recommended

## 🎯 AI Prompt Examples

### Cafe/Interior
```bash
python aimusic ai --prompt "cozy coffee shop with plants and warm lighting" --duration 120
```

### Night City
```bash
python aimusic ai --prompt "rainy night city with neon lights" --duration 180
```

### Bedroom/Study
```bash
python aimusic ai --prompt "bedroom with city view and desk setup" --duration 120
```

### Nature
```bash
python aimusic ai --prompt "peaceful forest with sunlight through trees" --duration 180
```

## 🔧 Troubleshooting

### Error: "No module named 'torch'"
```bash
pip install torch torchvision torchaudio
```

### Error: "No module named 'audiocraft'"
```bash
pip install audiocraft
```

### Error: "CUDA out of memory"
Use smaller models:
```bash
python aimusic ai --preset quick --prompt "test" --duration 30
```

### Too slow on CPU
Normal! AI on CPU is slow. Options:
1. Use `--preset quick` for smaller models
2. Reduce `--duration` to 30-60 seconds
3. Consider using GPU (NVIDIA)

### Models don't download
Check:
- Internet connection
- Disk space (20GB+)
- Firewall/proxy

## 📈 Performance

### With GPU (NVIDIA RTX 3060, 12GB VRAM)
- Music (30s): ~1-2 minutes
- Image: ~30-60 seconds
- Total: ~2-3 minutes

### Without GPU (CPU Intel i7)
- Music (30s): ~5-10 minutes
- Image: ~3-5 minutes
- Total: ~10-15 minutes

## 💡 Tips

1. **First time**: Use `--preset quick` to test
2. **Production**: Use `--preset balanced` or default models
3. **Maximum quality**: Use `--preset quality`
4. **Tests**: Use `--duration 30` to save time
5. **GPU**: Install CUDA Toolkit to accelerate

## 🔗 Useful Links

- [Install CUDA](https://developer.nvidia.com/cuda-downloads)
- [PyTorch](https://pytorch.org/get-started/locally/)
- [Hugging Face](https://huggingface.co/)
- [MusicGen](https://github.com/facebookresearch/audiocraft)
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion)

## ✅ Installation Checklist

- [ ] Python 3.9+ installed
- [ ] pip updated (`pip install --upgrade pip`)
- [ ] FFmpeg installed (`brew install ffmpeg`)
- [ ] requirements-full.txt installed
- [ ] 20GB+ free disk space
- [ ] NVIDIA GPU (optional, but recommended)
- [ ] CUDA Toolkit installed (if you have GPU)

## 🎉 Expected Result

With AI models installed, you will have:
- 🎵 Professional quality music
- 🎨 Realistic anime/lofi style images
- 🎬 YouTube-ready videos
- ⭐ Quality comparable to popular lofi channels

---

**Next step**: Run `python aimusic ai --prompt "cozy lofi music" --duration 60 --skip-upload`
