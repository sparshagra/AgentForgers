import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(override=True)

def generate_image_from_prompt(prompt: str, output_dir="outputs") -> str:
    """
    Generate an image using Stable Diffusion XL via Hugging Face InferenceClient.

    Args:
        prompt: Text description for image generation
        output_dir: Directory to save generated images

    Returns:
        Path to the saved image file
    """
    HF_TOKEN = os.environ.get("HF_TOKEN_3")
    assert HF_TOKEN, "HF_TOKEN must be set in environment"

    # Initialize the HF InferenceClient (calls router automatically)
    # client_image = InferenceClient(
    #     provider="nscale",
    #     api_key=HF_TOKEN,
    # )

    client_image = InferenceClient(
        provider="hf-inference",
        api_key=HF_TOKEN,
    )

    print(f"🎨 Generating image with prompt: {prompt[:100]}...")

    # Call the image generation API using the new structure (no requests.post)
    image = client_image.text_to_image(
        prompt,
        # model="stabilityai/stable-diffusion-xl-base-1.0",
        model="black-forest-labs/FLUX.1-schnell",
        num_inference_steps=30,
        guidance_scale=7.5,
    )

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_image_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    # Save the image
    image.save(filepath)

    print(f"✅  Saved image to {filepath}")
    return filepath

