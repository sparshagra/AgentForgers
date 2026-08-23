

from PIL import Image, ImageOps
import os

CANVAS_SIZE = 1080

def add_logo_to_image(input_image, logo_path, output_path, size_ratio=0.13, margin=40):
    """
    Adds a logo to the bottom-right corner of the generated image.
    Returns output_path.
    """

    if not os.path.exists(input_image):
        raise FileNotFoundError(f"Generated image not found: {input_image}")

    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo not found: {logo_path}")

    # Load generated image
    gen_img = Image.open(input_image).convert("RGBA")

    # Create White Square Canvas
    canvas = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (255, 255, 255, 255))
    resized = ImageOps.contain(gen_img, (CANVAS_SIZE, CANVAS_SIZE))

    x = (CANVAS_SIZE - resized.width) // 2
    y = (CANVAS_SIZE - resized.height) // 2
    canvas.paste(resized, (x, y), resized)

    # Add logo
    logo = Image.open(logo_path).convert("RGBA")

    new_w = int(CANVAS_SIZE * size_ratio)
    new_h = int(logo.height * (new_w / logo.width))

    logo = logo.resize((new_w, new_h), Image.LANCZOS)
    logo.putalpha(int(255 * 0.97))

    pos = (CANVAS_SIZE - new_w - margin, CANVAS_SIZE - new_h - margin)
    canvas.paste(logo, pos, logo)

    # Save Final
    canvas.save(output_path)
    return output_path
