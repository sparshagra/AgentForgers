import smtplib
import os
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes

def send_to_user(
    sender_email: str,
    sender_app_password: str,
    user_email: str,
    caption: str,
    hashtags: str,
    image_path: str,
    html_text: str
):
    """
    Send an approval email containing:
    - An attached image (final post)
    - HTML body with action links
    - Text caption for display

    Uses Gmail SMTP with App Password (required by Google).
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    msg = EmailMessage()
    msg["Subject"] = "Your Instagram Campaign Preview — Action Required"
    msg["From"] = sender_email
    msg["To"] = user_email

    # Attach both plaintext and HTML
    plain_text = (
        f"Caption:\n{caption}\n\n"
        f"Hashtags:\n{hashtags}\n\n"
        "Open the HTML email to choose Publish / Regenerate / Abort."
    )

    msg.set_content(plain_text)

    # Add HTML alternative
    msg.add_alternative(f"""
        <html>
            <body>
                <h2>Your Instagram Campaign Preview</h2>
                <p><b>Caption:</b> {caption}</p>
                <p><b>Hashtags:</b> {hashtags}</p>
                <hr>
                {html_text}
                <hr>
                <p>Image is attached below.</p>
            </body>
        </html>
    """, subtype="html")

    # Attach image
    with open(image_path, "rb") as f:
        img_data = f.read()

    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "image/png"  # safe fallback

    main_type, sub_type = mime_type.split("/")

    msg.add_attachment(
        img_data,
        maintype=main_type,
        subtype=sub_type,
        filename=os.path.basename(image_path)
    )

    # Connect to Gmail SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_app_password)
            smtp.send_message(msg)
            print(f"📧 Email sent successfully to {user_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise
