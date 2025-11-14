# from PIL import Image, ImageOps
# import os

# # ========= CONFIG =========
# GENERATED_IMAGE = "generated.png"   # <-- Path of your generated image
# LOGO_PATH = "brand_logo.png"        # <-- Path of your logo
# OUTPUT_PATH = "final_post.png"
# CANVAS_SIZE = 1080                  # Final Instagram square
# # ==========================


# # ======================================
# # STEP 1 — Load Generated Image
# # ======================================
# if not os.path.exists(GENERATED_IMAGE):
#     raise ValueError("❌ Generated image not found!")

# gen_img = Image.open(GENERATED_IMAGE).convert("RGBA")

# # ======================================
# # STEP 2 — Create Clean White Template
# # ======================================
# def create_white_canvas(size=1080):
#     return Image.new("RGBA", (size, size), (255, 255, 255, 255))

# canvas = create_white_canvas(CANVAS_SIZE)

# # Resize generated image while keeping aspect ratio
# gen_img_resized = ImageOps.contain(gen_img, (CANVAS_SIZE, CANVAS_SIZE))

# # Paste centered
# x = (CANVAS_SIZE - gen_img_resized.width) // 2
# y = (CANVAS_SIZE - gen_img_resized.height) // 2
# canvas.paste(gen_img_resized, (x, y), gen_img_resized)

# print("🖼 Placed generated image onto white canvas.")


# # ======================================
# # STEP 3 — Add Logo (Pillow 10+ Compatible)
# # ======================================
# def overlay_logo(base_img, logo_path, margin=40, size_ratio=0.13, opacity=0.95):
#     base = base_img.copy()
#     W, H = base.size

#     if not os.path.exists(logo_path):
#         raise ValueError("❌ Logo file not found!")

#     logo = Image.open(logo_path).convert("RGBA")

#     # Resize logo based on image width
#     new_w = int(W * size_ratio)
#     new_h = int(logo.height * (new_w / logo.width))

#     # Use LANCZOS instead of deprecated ANTIALIAS
#     logo = logo.resize((new_w, new_h), Image.LANCZOS)
#     logo.putalpha(int(255 * opacity))

#     # Bottom-right position
#     pos = (W - new_w - margin, H - new_h - margin)
#     base.paste(logo, pos, logo)
#     return base


# # Overlay logo
# final_post = overlay_logo(canvas, LOGO_PATH)
# final_post.save(OUTPUT_PATH)

# print(f"\n🎉 FINAL BRAND POST SAVED → {OUTPUT_PATH}")


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
