#!/usr/bin/env python3
"""
Music generator using multiple AI models
"""

import argparse
import os
import yaml
import torch


def load_models_config():
    with open("models_config.yaml", "r") as f:
        return yaml.safe_load(f)


def generate_with_musicgen(model_id, prompt, duration, output_path):
    """Generates music using MusicGen"""
    import torch
    from audiocraft.models import MusicGen
    from audiocraft.data.audio import audio_write

    print(f"🎵 Loading MusicGen ({model_id})...")

    # Device selection
    # Note: MusicGen doesn't support MPS (Apple Silicon) due to missing operators
    # (weight_norm, autocast). Using CPU on Mac is actually faster than MPS fallback.
    if torch.cuda.is_available():
        device = "cuda"
        print("🚀 Using NVIDIA GPU (CUDA)")
    else:
        device = "cpu"
        if torch.backends.mps.is_available():
            print("💻 Using CPU (MusicGen doesn't support Apple Silicon GPU yet)")
            print("⏳ Expected time: ~2-3 minutes for 30s, ~5-10 minutes for 60s")
        else:
            print("💻 Using CPU")
            print("⏳ This may take several minutes...")

    # Load model
    print("📦 Loading model weights...")
    model = MusicGen.get_pretrained(model_id, device=device)
    model.set_generation_params(duration=duration)

    print(f"🎼 Generating {duration}s of music: '{prompt}'...")
    print("⏳ Please be patient, generation in progress...")

    import time

    start_time = time.time()

    wav = model.generate([prompt])

    elapsed = time.time() - start_time
    print(f"✅ Generation completed in {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")

    print("💾 Saving music...")
    audio_write(output_path, wav[0].cpu(), model.sample_rate, strategy="loudness")

    return f"{output_path}.wav"


def generate_with_audioldm(model_id, prompt, duration, output_path):
    """Generate music using AudioLDM"""
    from diffusers import AudioLDMPipeline

    print(f"🎵 Loading AudioLDM ({model_id})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = AudioLDMPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
    pipe = pipe.to(device)

    print(f"🎼 Generating music: '{prompt}'...")
    audio = pipe(prompt, num_inference_steps=50, audio_length_in_s=duration).audios[0]

    # Save audio
    import scipy.io.wavfile as wavfile

    sample_rate = 16000
    output_file = f"{output_path}.wav"
    wavfile.write(output_file, sample_rate, audio)

    print(f"💾 Music saved to {output_file}")
    return output_file


def generate_with_riffusion(model_id, prompt, duration, output_path):
    """Generate music using Riffusion"""
    from diffusers import StableDiffusionPipeline

    print(f"🎵 Loading Riffusion ({model_id})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)

    print(f"🎼 Generating spectrogram: '{prompt}'...")
    # Riffusion generates spectrograms that are converted to audio
    _ = pipe(prompt).images[0]  # noqa: F841

    # Convert spectrogram to audio (simplified)
    # In production, use the complete riffusion library
    print("⚠️  Riffusion requires additional spectrogram to audio conversion")
    print("💡 Use MusicGen or AudioLDM for better support")

    return None


def generate_music_ai(prompt, duration=30, output_path="output/music", model_key="musicgen-small"):
    """Generate music using the specified model"""

    models_config = load_models_config()

    if model_key not in models_config["music_models"]:
        print(f"❌ Model '{model_key}' not found!")
        print("💡 Use: python list_models.py to see available models")
        return None

    model_info = models_config["music_models"][model_key]
    model_id = model_info["model_id"]

    print(f"\n{'='*60}")
    print("🎵 Generating Music with AI")
    print(f"{'='*60}")
    print(f"Model: {model_info['name']}")
    print(f"Quality: {model_info['quality']}")
    print(f"Size: {model_info['size']}")
    print(f"GPU: {'Required' if model_info['gpu_required'] else 'Optional'}")
    print(f"{'='*60}\n")

    # Create output directory
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    # Select generator based on model
    try:
        if "musicgen" in model_key:
            return generate_with_musicgen(model_id, prompt, duration, output_path)
        elif "audioldm" in model_key:
            return generate_with_audioldm(model_id, prompt, duration, output_path)
        elif "riffusion" in model_key:
            return generate_with_riffusion(model_id, prompt, duration, output_path)
        else:
            print(f"❌ Generator not implemented for {model_key}")
            return None
    except ImportError as e:
        print("❌ Error: Required libraries not installed")
        print("💡 Run: pip install -r requirements-full.txt")
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error generating music: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate music with AI (multiple models)")
    parser.add_argument("--prompt", type=str, required=True, help="Music description")
    parser.add_argument("--duration", type=int, default=30, help="Duration in seconds")
    parser.add_argument("--output", type=str, default="output/music", help="Output path")
    parser.add_argument("--model", type=str, default="musicgen-small", help="Model a usar (see list_models.py)")

    args = parser.parse_args()

    result = generate_music_ai(args.prompt, args.duration, args.output, args.model)

    if result:
        print(f"\n✅ Music generated successfully: {result}")
    else:
        print("\n❌ Failed to generate music")


if __name__ == "__main__":
    main()
