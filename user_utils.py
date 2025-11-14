import os
import json
import hashlib

USER_BASE_DIR = "users"
os.makedirs(USER_BASE_DIR, exist_ok=True)

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def user_folder(username: str) -> str:
    return os.path.join(USER_BASE_DIR, username)

def ensure_user_exists(username: str):
    path = user_folder(username)
    if not os.path.exists(path):
        raise FileNotFoundError(f"User '{username}' does not exist.")
    return path

def ensure_unique_username(username: str):
    path = user_folder(username)
    if os.path.exists(path):
        raise ValueError("Username already exists.")
    os.makedirs(path)

def save_login(username, password, gmail, insta_id, insta_pw):
    path = user_folder(username)
    with open(os.path.join(path, "login.json"), "w") as f:
        json.dump({
            "password_hash": hash_pw(password),
            "gmail": gmail,
            "insta_id": insta_id,
            "insta_pw": insta_pw
        }, f)

def save_brand(username, brand_details, brand_idea):
    path = ensure_user_exists(username)
    with open(os.path.join(path, "brand.json"), "w") as f:
        json.dump({
            "brand_details": brand_details,
            "brand_idea": brand_idea
        }, f)

def save_logo(username, file_bytes):
    path = ensure_user_exists(username)
    logo_path = os.path.join(path, "logo.png")
    with open(logo_path, "wb") as f:
        f.write(file_bytes)
    return logo_path

def load_login(username):
    path = ensure_user_exists(username)
    with open(os.path.join(path, "login.json")) as f:
        return json.load(f)

def load_brand(username):
    path = ensure_user_exists(username)
    with open(os.path.join(path, "brand.json")) as f:
        return json.load(f)

def load_logo_path(username):
    path = ensure_user_exists(username)
    logo = os.path.join(path, "logo.png")
    return logo if os.path.exists(logo) else None

def check_password(username, password):
    data = load_login(username)
    return data["password_hash"] == hash_pw(password)

def fetch_full_profile(username):
    login = load_login(username)
    brand = load_brand(username)
    logo_path = load_logo_path(username)
    return {
        "username": username,
        "gmail": login["gmail"],
        "insta_id": login["insta_id"],
        "insta_pw": login["insta_pw"],
        "brand_details": brand["brand_details"],
        "brand_idea": brand["brand_idea"],
        "logo": logo_path
    }
