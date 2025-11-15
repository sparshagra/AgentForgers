from instagrapi import Client

def post_to_instagram(username, password, image_path, caption):
    """
    Post an image to Instagram using instagrapi.

    Args:
        username (str): Instagram username.
        password (str): Instagram password.
        image_path (str): Local image file path.
        caption (str): Caption text.
    """
    final_image = image_path
    cl = Client()

    try:
        cl.login(username, password)
    except Exception as e:
        print("❌ Instagram login failed:", e)
        raise

    try:
        cl.photo_upload(final_image, caption)
        print("📸 Posted successfully to Instagram")
    except Exception as e:
        print("❌ Instagram posting failed:", e)
        raise
