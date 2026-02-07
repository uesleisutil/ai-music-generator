# 🤖 AI Models Guide - AWS Cloud

This guide explains the AI models used in the cloud pipeline and how to choose the best ones for your needs.

---

## 🎵 Music Models

All models run on AWS with NVIDIA GPU acceleration (CUDA support).

### MusicGen (Meta/Facebook) - Recommended

**musicgen-small** (300MB)
- ✅ Fast generation (~1-2 min for 60s)
- ✅ Works well on CPU if needed
- ⚠️ Basic quality
- 💰 Cheapest option
- **Use case**: Quick tests, high volume

**musicgen-medium** (1.5GB) ⭐ **RECOMMENDED**
- ✅ Excellent quality
- ✅ Good speed (~2-3 min for 60s)
- ✅ Best balance quality/cost
- 💰 ~$0.02 per video
- **Use case**: Production, default choice

**musicgen-large** (3.3GB)
- ✅ Best quality
- ⚠️ Slower (~4-5 min for 60s)
- ⚠️ Requires more memory
- 💰 ~$0.03 per video
- **Use case**: Maximum quality needed

**musicgen-melody** (1.5GB)
- ✅ Specialized in melodies
- ✅ Can use reference audio
- ✅ Good for specific styles
- **Use case**: Melody-focused music

### AudioLDM (CVSSP)

**audioldm** (1.2GB)
- ✅ Fast generation
- ✅ Good for sound effects
- ✅ Alternative style
- **Use case**: Experimental sounds

**audioldm-large** (2.5GB)
- ✅ Better quality than standard
- ✅ More detailed audio
- **Use case**: High-quality sound effects

### Riffusion

**riffusion** (2GB)
- ✅ Unique spectrogram-based approach
- ✅ Interesting artistic style
- ⚠️ Experimental
- **Use case**: Unique/experimental music

---

## 🎨 Image Models

All models generate lofi/anime style covers optimized for music videos.

### Stable Diffusion (Stability AI)

**sd-2-1** (5GB) ⭐ **RECOMMENDED**
- ✅ Excellent quality
- ✅ Fast generation (~30-60s)
- ✅ Great for lofi/anime style
- ✅ Reliable and stable
- **Use case**: Default choice, production

**sd-xl-base** (7GB)
- ✅ Best quality available
- ✅ More detailed images
- ⚠️ Slower (~1-2 min)
- ⚠️ Requires more memory
- **Use case**: Maximum quality

**sd-1-5** (4GB)
- ✅ Lighter and faster
- ✅ Good quality
- ✅ Lower memory usage
- **Use case**: Budget-conscious

### Alternative Models

**kandinsky-2-2** (5GB)
- ✅ Unique artistic style
- ✅ Great for covers
- ✅ Different aesthetic
- **Use case**: Artistic variation

**wuerstchen** (3GB)
- ✅ Very fast
- ✅ Compact model
- ✅ Good quality
- **Use case**: Quick generation

**deepfloyd-if** (8GB)
- ✅ Photorealistic quality
- ✅ Best for professional covers
- ⚠️ Largest model
- ⚠️ Slowest generation
- **Use case**: Premium quality

---

## 🎯 Presets

Presets combine music and image models for specific use cases.

### Quick
```bash
--preset quick
```
- **Music**: musicgen-small (300MB)
- **Image**: wuerstchen (3GB)
- **Speed**: ⚡⚡⚡ Very fast (~2 min)
- **Quality**: ⭐⭐⭐ Good
- **Cost**: 💰 ~$0.015/video
- **Use case**: Testing, high volume

### Balanced ⭐ **RECOMMENDED**
```bash
--preset balanced
```
- **Music**: musicgen-medium (1.5GB)
- **Image**: sd-2-1 (5GB)
- **Speed**: ⚡⚡ Fast (~3 min)
- **Quality**: ⭐⭐⭐⭐ Excellent
- **Cost**: 💰 ~$0.02/video
- **Use case**: Production, default

### Quality
```bash
--preset quality
```
- **Music**: musicgen-large (3.3GB)
- **Image**: sd-xl-base (7GB)
- **Speed**: ⚡ Medium (~5 min)
- **Quality**: ⭐⭐⭐⭐⭐ Best
- **Cost**: 💰 ~$0.03/video
- **Use case**: Premium content

### Experimental
```bash
--preset experimental
```
- **Music**: riffusion (2GB)
- **Image**: kandinsky-2-2 (5GB)
- **Speed**: ⚡⚡ Fast (~3 min)
- **Quality**: ⭐⭐⭐⭐ Unique
- **Cost**: 💰 ~$0.02/video
- **Use case**: Artistic variation

---

## 📊 Performance Comparison

### On AWS (g4dn.xlarge - NVIDIA T4)

| Preset | Music Time | Image Time | Total Time | Cost |
|--------|-----------|------------|------------|------|
| Quick | 1-2 min | 20-30s | ~2 min | $0.015 |
| Balanced | 2-3 min | 30-60s | ~3 min | $0.02 |
| Quality | 4-5 min | 1-2 min | ~5 min | $0.03 |
| Experimental | 2-3 min | 30-60s | ~3 min | $0.02 |

**Note**: Times are for 60 seconds of music. Shorter durations are proportionally faster.

---

## 🎨 Image Style Optimization

All image models are optimized with enhanced prompts for lofi/anime aesthetic:

### Automatic Enhancements

Your prompt:
```
"cozy coffee shop"
```

Enhanced prompt (automatic):
```
"cozy coffee shop, lofi aesthetic, anime style, studio ghibli inspired, 
warm lighting, soft colors, detailed background, makoto shinkai style, 
high quality, 4k, artistic"
```

### Style Keywords

Add these to your prompts for specific styles:

**Anime/Lofi**:
- `studio ghibli style`
- `makoto shinkai style`
- `lofi aesthetic`
- `anime background`

**Lighting**:
- `warm lighting`
- `soft lighting`
- `golden hour`
- `neon lights`

**Mood**:
- `cozy atmosphere`
- `peaceful mood`
- `relaxing vibe`
- `nostalgic feeling`

**Quality**:
- `high quality`
- `detailed`
- `4k`
- `professional`

---

## 🎯 Choosing the Right Models

### For Testing
```bash
python aws_submit_job.py \
  --preset quick \
  --duration 30 \
  --output-bucket your-bucket
```

### For Production (Recommended)
```bash
python aws_submit_job.py \
  --preset balanced \
  --duration 60 \
  --output-bucket your-bucket
```

### For Maximum Quality
```bash
python aws_submit_job.py \
  --preset quality \
  --duration 90 \
  --output-bucket your-bucket
```

### Custom Models
```bash
python aws_submit_job.py \
  --prompt "your prompt" \
  --duration 60 \
  --output-bucket your-bucket
  # Uses default: musicgen-medium + sd-2-1
```

---

## 💡 Tips

1. **Start with balanced**: Best quality/cost ratio
2. **Use quick for testing**: Fast and cheap
3. **Use quality for premium**: When quality matters most
4. **Batch similar jobs**: Generate multiple videos in one session
5. **Monitor costs**: Check AWS billing regularly

---

## 📚 Model Documentation

- [MusicGen](https://github.com/facebookresearch/audiocraft) - Meta's music generation
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) - Image generation
- [AudioLDM](https://github.com/haoheliu/AudioLDM) - Audio generation
- [Riffusion](https://www.riffusion.com/) - Spectrogram-based music

---

## 🔧 Advanced: Custom Model Selection

You can specify exact models in the job submission (requires modifying `aws_batch_worker.py`):

```python
# In aws_batch_worker.py, modify job_config:
job_config = {
    'music_model': 'musicgen-large',
    'image_model': 'sd-xl-base',
    # ...
}
```

---

**Recommendation**: Use `--preset balanced` for 95% of use cases. It provides excellent quality at minimal cost (~$0.02/video).
