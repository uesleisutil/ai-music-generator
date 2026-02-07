# Setup Guide

## 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## 2. Install FFmpeg

### macOS
```bash
brew install ffmpeg
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows
Download from: https://ffmpeg.org/download.html

## 3. Configure YouTube API

1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Download the JSON file and rename to `client_secrets.json`
6. Place in project root

## 4. First Use

```bash
# Simple test (30 seconds)
python pipeline.py --prompt "cozy lofi home music" --duration 30 --title "Cozy Lofi Music"
```

First time, a browser will open for you to authorize YouTube access.

## Tips

- **GPU**: If you have NVIDIA GPU, install CUDA to accelerate generation
- **Duration**: Start with 30s to test, then increase
- **Models**: 
  - `musicgen-small`: Faster, less quality
  - `musicgen-medium`: Balanced
  - `musicgen-large`: Best quality, slower

## Troubleshooting

### Memory error
- Use `musicgen-small` in config.yaml
- Reduce music duration
- Close other programs

### FFmpeg not found
- Check if it's in PATH: `ffmpeg -version`
- Reinstall FFmpeg

### YouTube authentication error
- Check if `client_secrets.json` is correct
- Delete `token.pickle` and try again
