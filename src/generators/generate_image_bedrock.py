#!/usr/bin/env python3
"""
Image generator using AWS Bedrock (Stable Diffusion XL and Titan)
"""

import argparse
import os
import json
import base64
import boto3


def generate_with_bedrock_sdxl(prompt, output_path, width=1280, height=720):
    """Generate image using Stable Diffusion XL via AWS Bedrock"""

    print("🎨 Generating image with AWS Bedrock (Stable Diffusion XL)...")
    print(f"   Resolution: {width}x{height}")

    # Initialize Bedrock client
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Enhance prompt for lofi/anime style
    enhanced_prompt = enhance_prompt_for_lofi(prompt)

    # Prepare request body for SDXL
    body = json.dumps(
        {
            "text_prompts": [
                {"text": enhanced_prompt, "weight": 1.0},
                {
                    "text": "blurry, low quality, distorted, ugly, bad anatomy, watermark, text, signature",
                    "weight": -1.0,
                },
            ],
            "cfg_scale": 8.5,
            "steps": 50,
            "seed": 0,
            "width": width,
            "height": height,
            "samples": 1,
        }
    )

    # Model ID for Stable Diffusion XL
    model_id = "stability.stable-diffusion-xl-v1"

    try:
        print("🔄 Calling Bedrock API...")
        response = bedrock_runtime.invoke_model(
            modelId=model_id, body=body, contentType="application/json", accept="application/json"
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Get base64 image
        image_base64 = response_body["artifacts"][0]["base64"]

        # Decode and save
        image_data = base64.b64decode(image_base64)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"✅ Image generated successfully: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error calling Bedrock: {e}")
        return None


def generate_with_bedrock_titan(prompt, output_path, width=1280, height=720):
    """Generate image using Amazon Titan Image Generator via AWS Bedrock"""

    print("🎨 Generating image with AWS Bedrock (Amazon Titan)...")
    print(f"   Resolution: {width}x{height}")

    # Initialize Bedrock client
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Enhance prompt for lofi/anime style
    enhanced_prompt = enhance_prompt_for_lofi(prompt)

    # Prepare request body for Titan
    body = json.dumps(
        {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": enhanced_prompt,
                "negativeText": "blurry, low quality, distorted, ugly, bad anatomy, watermark, text, signature",
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "premium",
                "height": height,
                "width": width,
                "cfgScale": 8.0,
                "seed": 0,
            },
        }
    )

    # Model ID for Amazon Titan
    model_id = "amazon.titan-image-generator-v1"

    try:
        print("🔄 Calling Bedrock API...")
        response = bedrock_runtime.invoke_model(
            modelId=model_id, body=body, contentType="application/json", accept="application/json"
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Get base64 image
        image_base64 = response_body["images"][0]

        # Decode and save
        image_data = base64.b64decode(image_base64)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"✅ Image generated successfully: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error calling Bedrock: {e}")
        return None


def enhance_prompt_for_lofi(prompt):
    """Enhance prompt to generate high quality lofi/chill style images"""

    prompt_lower = prompt.lower()

    # Base quality
    base_quality = "masterpiece, best quality, highly detailed, professional, 4k, sharp focus, vibrant colors"

    # Lofi/anime style
    lofi_style = "lofi aesthetic, anime art style, studio ghibli inspired, makoto shinkai style"
    lofi_style += ", soft lighting, warm color palette, cozy atmosphere, dreamy, atmospheric, cinematic"

    # Scene-specific enhancements
    if "coffee" in prompt_lower or "cafe" in prompt_lower:
        scene = "cozy coffee shop interior, large windows with sunlight, wooden furniture, plants"
        scene += ", warm ambient lighting, peaceful atmosphere, vintage decor"
        enhanced = f"{scene}, {prompt}, {lofi_style}, {base_quality}"

    elif "rain" in prompt_lower or "rainy" in prompt_lower:
        scene = "rainy night cityscape, rain drops on window, wet streets with reflections"
        scene += ", neon lights, moody atmosphere, purple and blue tones, cinematic lighting"
        enhanced = f"{scene}, {prompt}, {lofi_style}, {base_quality}"

    elif "night" in prompt_lower or "city" in prompt_lower:
        scene = "night time urban landscape, city skyline, neon signs glowing"
        scene += ", purple and pink color scheme, atmospheric, detailed architecture, starry sky"
        enhanced = f"{scene}, {prompt}, {lofi_style}, {base_quality}"

    elif "forest" in prompt_lower or "nature" in prompt_lower:
        scene = "peaceful forest scene, sunlight through trees, lush vegetation"
        scene += ", natural lighting, serene atmosphere, detailed foliage"
        enhanced = f"{scene}, {prompt}, {lofi_style}, {base_quality}"

    else:
        # Generic lofi scene
        scene = "lofi scene, detailed background, atmospheric lighting, depth, perspective"
        enhanced = f"{scene}, {prompt}, {lofi_style}, {base_quality}"

    return enhanced


def generate_image_bedrock(prompt, output_path="output/cover.png", model="sdxl", width=1280, height=720):
    """Generate image using AWS Bedrock"""

    print(f"\n{'='*60}")
    print("🎨 AWS Bedrock Image Generation")
    print(f"{'='*60}")
    print(f"Model: {model.upper()}")
    print(f"Resolution: {width}x{height}")
    print(f"Prompt: {prompt}")
    print(f"{'='*60}\n")

    if model == "sdxl":
        return generate_with_bedrock_sdxl(prompt, output_path, width, height)
    elif model == "titan":
        return generate_with_bedrock_titan(prompt, output_path, width, height)
    else:
        print(f"❌ Unknown model: {model}")
        print("💡 Available models: sdxl, titan")
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate image with AWS Bedrock")
    parser.add_argument("--prompt", type=str, required=True, help="Image description")
    parser.add_argument("--output", type=str, default="output/cover.png", help="Output path")
    parser.add_argument(
        "--model",
        type=str,
        default="sdxl",
        choices=["sdxl", "titan"],
        help="Bedrock model: sdxl (Stable Diffusion XL) or titan (Amazon Titan)",
    )
    parser.add_argument("--width", type=int, default=1280, help="Image width")
    parser.add_argument("--height", type=int, default=720, help="Image height")

    args = parser.parse_args()

    result = generate_image_bedrock(args.prompt, args.output, args.model, args.width, args.height)

    if result:
        print(f"\n✅ Image generated successfully: {result}")
    else:
        print("\n❌ Failed to generate image")


if __name__ == "__main__":
    main()
