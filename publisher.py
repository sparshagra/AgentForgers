# from send import send_to_user  # Email function
# from insta import post_to_instagram  # IG posting

# def send_approval_email(campaign_id, user_email, campaign_data):
#     # Compose and send approval email
#     html_message = f"""
#         {campaign_data['description']}
#         <br><b>Caption:</b> {campaign_data['caption']}
#         <br><b>Hashtags:</b> {campaign_data['hashtags']}
#         <br>Choose: ✅ Publish | 🔄 Regenerate | ❌ Delete
#     """
#     send_to_user(
#         sender_email=campaign_data['sender_email'],
#         sender_app_password=campaign_data['sender_app_password'],
#         user_email=user_email,
#         caption=campaign_data['caption'],
#         hashtags=campaign_data['hashtags'],
#         image_path=campaign_data['image_path'],
#         html_text=html_message
#     )
#     return True

# def publish_to_instagram(ig_username, ig_password, image_path, caption, hashtags):
#     # Handle IG posting and OTP/exceptions
#     post_to_instagram(ig_username, ig_password, image_path, f"{caption}\n{hashtags}")
#     return True
# publisher.py

import os
from email_sender import send_to_user
 # Email function
from insta_local import post_to_instagram
 # IG posting


def _build_caption_strings(caption_data):
    """
    Accepts either:
    - dict: { "caption": str, "description": str, "hashtags": [..] }
    - or a plain string
    Returns: (caption_text, description_text, hashtags_str, full_caption_for_post)
    """
    if isinstance(caption_data, dict):
        cap = caption_data.get("caption", "") or ""
        desc = caption_data.get("description", "") or ""
        hashtags = caption_data.get("hashtags") or []
        if isinstance(hashtags, list):
            hashtags_str = " ".join(str(h) for h in hashtags)
        else:
            hashtags_str = str(hashtags)
    else:
        # Fallback: treat whole thing as caption
        cap = str(caption_data)
        desc = ""
        hashtags_str = ""

    full_caption = cap
    if desc:
        full_caption = (full_caption + "\n\n" + desc).strip()
    if hashtags_str:
        full_caption = (full_caption + "\n\n" + hashtags_str).strip()

    return cap, desc, hashtags_str, full_caption


def send_approval_email(campaign_id, user_email, campaign_data):
    """
    Compose and send approval email with 3 choices:
    - Publish
    - Regenerate
    - Abort

    campaign_data must include:
    - caption (dict or str)
    - image_path
    - sender_email
    - sender_app_password
    - optional: festival_name
    """
    base_url = os.environ.get("APP_BASE_URL", "http://localhost:8000")

    caption_data = campaign_data.get("caption", "")
    festival_name = campaign_data.get("festival_name", "")

    cap, desc, hashtags_str, full_caption = _build_caption_strings(caption_data)

    publish_url = f"{base_url}/scheduler/publish/{campaign_id}"
    regen_url = f"{base_url}/scheduler/regenerate/{campaign_id}"
    abort_url = f"{base_url}/scheduler/abort/{campaign_id}"

    html_message = f"""
        <p><b>Campaign ID:</b> {campaign_id}</p>
        <p><b>Festival:</b> {festival_name}</p>
        <p><b>Description:</b> {desc or '(none)'}</p>
        <p><b>Caption:</b> {cap}</p>
        <p><b>Hashtags:</b> {hashtags_str or '(none)'}</p>
        <hr>
        <p><b>Actions:</b></p>
        <p>
           ✅ <a href="{publish_url}">Publish</a><br>
           🔄 <a href="{regen_url}">Regenerate</a><br>
           ❌ <a href="{abort_url}">Abort</a>
        </p>
    """

    send_to_user(
        sender_email=campaign_data["sender_email"],
        sender_app_password=campaign_data["sender_app_password"],
        user_email=user_email,
        caption=full_caption,
        hashtags=hashtags_str,
        image_path=campaign_data["image_path"],
        html_text=html_message
    )
    return True


def publish_to_instagram(ig_username, ig_password, caption_data, image_path):
    """
    Post to Instagram using the given caption structure and image path.
    caption_data can be dict or string.
    """
    cap, desc, hashtags_str, full_caption = _build_caption_strings(caption_data)

    # Here full_caption already includes hashtags_str, but we pass both for backwards compatibility
    post_to_instagram(
        ig_username,
        ig_password,
        image_path,
        full_caption
    )
    return True
