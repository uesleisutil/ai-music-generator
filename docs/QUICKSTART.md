# 🚀 Quick Start Guide

## Quick Installation

```bash
# Clone the repository
git clone https://github.com/uesleisutil/ai-music-generator.git
cd ai-music-generator

# Install basic dependencies
pip install -r requirements.txt

# Install FFmpeg (if you don't have it)
brew install ffmpeg  # macOS
```

## Quick Test (Without AI)

To quickly test the system without installing heavy AI models:

```bash
python pipeline_simple.py \
  --prompt "cozy lofi music" \
  --duration 30 \
  --title "My First Test" \
  --skip-upload
```

This will generate:
- ✅ Test music (simple audio synthesis)
- ✅ Cover image (gradient with text)
- ✅ Complete video (music + image)

**Files generated in:** `output/`

## Full Mode (With AI)

To use real AI models (GPU recommended):

### 1. Install AI Models

```bash
pip install -r requirements-full.txt
```

⚠️ **Warning:** This will download ~10GB of models. May take a while!

### 2. Generate Music with AI

```bash
python pipeline.py \
  --prompt "cozy lofi home music with rain sounds" \
  --duration 180 \
  --title "Cozy Lofi Beats" \
  --skip-upload
```

## Upload to YouTube

### 1. Configure YouTube API

1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Download the JSON file and rename to `client_secrets.json`
6. Place in project root

### 2. Upload

```bash
# Without --skip-upload
python pipeline_simple.py \
  --prompt "relaxing music" \
  --duration 60 \
  --title "Relaxing Music" \
  --privacy unlisted
```

First time, a browser will open to authorize access.

## Useful Commands

### Generate Music Only
```bash
python generate_music_simple.py --prompt "jazz piano" --duration 60
```

### Generate Image Only
```bash
python generate_image_simple.py --prompt "jazz piano album cover"
```

### Create Video from Existing Files
```bash
python create_video.py \
  --audio output/music.wav \
  --image output/cover.png \
  --output my_video.mp4
```

## Privacy Options

- `--privacy public` - Public (everyone can see)
- `--privacy unlisted` - Unlisted (only with link)
- `--privacy private` - Private (only you)

## Troubleshooting

### Error: FFmpeg not found
```bash
# Install FFmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

### Error: Insufficient memory
Use simple mode or reduce duration:
```bash
python pipeline_simple.py --prompt "test" --duration 10 --skip-upload
```

### Error: client_secrets.json not found
You only need this for YouTube upload. Use `--skip-upload` to skip.

## Next Steps

1. ✅ Test simple mode
2. ✅ Check files in `output/`
3. ⚙️ Configure YouTube API (optional)
4. 🚀 Install complete AI models (optional)
5. 🎵 Create your music!

## Prompt Examples

**Lofi/Chill:**
- "cozy lofi home music with rain sounds"
- "chill beats to study and relax"
- "peaceful lofi hip hop"

**Energetic:**
- "upbeat electronic dance music"
- "energetic rock guitar solo"
- "fast-paced techno beats"

**Classical:**
- "calm piano meditation music"
- "smooth jazz saxophone evening"
- "epic orchestral cinematic music"

## Help

- 📖 Complete documentation: [README.md](README.md)
- 🔧 Installation guide: [SETUP.md](SETUP.md)
- 🐛 Report bugs: [Issues](https://github.com/uesleisutil/ai-music-generator/issues)

---

**Tip:** Always start with `--duration 10` and `--skip-upload` for quick tests!
