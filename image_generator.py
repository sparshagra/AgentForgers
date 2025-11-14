import os
from huggingface_hub import InferenceClient

HF_TOKEN = os.environ["HF_TOKEN_3"]

client_image = InferenceClient(
    # provider="nscale",
    provider="hf-inference",
    api_key=HF_TOKEN,
)

def generate_image_sd(prompt: str, output_path: str = "campaign_image.png"):
    print("\n🎨  Generating image via Hugging Face Inference API…")
    image = client_image.text_to_image(
        prompt,
        # model="stabilityai/stable-diffusion-xl-base-1.0",
        model="black-forest-labs/FLUX.1-dev",
    )
    image.save(output_path)
    print(f"✅  Saved image to {output_path}")
    return output_path
