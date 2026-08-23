from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.storage.user_utils import (
    ensure_unique_username,
    save_login,
    save_brand,
    save_logo,
    check_password,
    fetch_full_profile,
    ensure_user_exists,
    load_brand,
    load_logo_path,
)

from backend.graph.workflow_runner import run_workflow
from backend.scheduling.scheduler_utils import (
    create_task,
    get_due_tasks,
    load_task,
    save_task,
)
from backend.publishing.publisher import send_approval_email, publish_to_instagram

import os
import json
from datetime import datetime


# --------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

app = FastAPI()

# CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure folders exist
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
USERS_DIR = "users"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(USERS_DIR, exist_ok=True)

# Serve static files so frontend can fetch images/logos
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")
app.mount("/users", StaticFiles(directory=USERS_DIR), name="users")


# --------------------------------------------------------------------------
# USER MANAGEMENT ENDPOINTS
# --------------------------------------------------------------------------

@app.post("/register")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    gmail: str = Form(...),
    insta_id: str = Form(...),
    insta_pw: str = Form(...),
    brand_details: str = Form(...),
    brand_idea: str = Form(...),
    logo: UploadFile = File(...),
):
    # Username MUST be unique
    try:
        ensure_unique_username(username)
    except ValueError:
        raise HTTPException(400, "Username already exists.")

    # Save login details
    save_login(username, password, gmail, insta_id, insta_pw)

    # Save brand details
    save_brand(username, brand_details, brand_idea)

    # Save logo (stored in users/<username>/logo.png)
    logo_bytes = await logo.read()
    save_logo(username, logo_bytes)

    return {"status": "registered", "username": username}


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        ensure_user_exists(username)
    except FileNotFoundError:
        raise HTTPException(404, "User not found")

    if not check_password(username, password):
        raise HTTPException(401, "Invalid password")

    profile = fetch_full_profile(username)
    return {"status": "logged_in", "profile": profile}


@app.get("/user/{username}/profile")
async def get_profile(username: str):
    try:
        profile = fetch_full_profile(username)
    except Exception as e:
        raise HTTPException(404, str(e))
    return profile


@app.post("/user/update_brand")
async def update_brand(
    username: str = Form(...),
    brand_details: str = Form(None),
    brand_idea: str = Form(None),
    logo: UploadFile = File(None),
):
    try:
        ensure_user_exists(username)
    except Exception as e:
        raise HTTPException(404, str(e))

    if brand_details or brand_idea:
        existing = load_brand(username)
        save_brand(
            username,
            brand_details or existing["brand_details"],
            brand_idea or existing["brand_idea"],
        )

    logo_path = None
    if logo:
        bytes_data = await logo.read()
        logo_path = save_logo(username, bytes_data)

    return {
        "status": "brand_updated",
        "logo_updated": bool(logo),
        "logo_path": logo_path,
    }


@app.get("/user/fetch")
async def fetch_user(username: str):
    try:
        return fetch_full_profile(username)
    except Exception as e:
        raise HTTPException(404, str(e))


# --------------------------------------------------------------------------
# WORKFLOW ENDPOINT (Option 1 – interactive)
# --------------------------------------------------------------------------

@app.post("/run_workflow")
async def run_workflow_endpoint(
    user_prompt: str = Form(...),
    username: str = Form(None),   # allow passing username
    logo: UploadFile = File(None),
    context: str = Form("{}"),
):
    logo_path = None

    # If user is known → auto-load their stored logo
    if username:
        try:
            logo_path = load_logo_path(username)
        except Exception:
            logo_path = None

    # If logo is uploaded, override the user’s stored logo
    if logo:
        # we save override logo also under users/<username>/logo.png
        bytes_data = await logo.read()
        if not username:
            raise HTTPException(400, "Username is required when uploading a logo.")
        logo_path = save_logo(username, bytes_data)

    # Parse context
    try:
        user_context = json.loads(context)
        if not isinstance(user_context, dict):
            raise ValueError()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid context JSON."},
        )

    # Pass logo path into workflow context (used for logo drop)
    if logo_path:
        user_context["logo_path"] = logo_path

    # Run the LangGraph workflow
    result = run_workflow(user_prompt, context=user_context)

    # Local file path for the generated final image (used by scheduler & publishing)
    image_path = result.get("generated_image")
    caption = result.get("caption")
    timeline = result.get("timeline", [])

    # Public URL for frontend preview
    image_url = None
    if image_path:
        filename = os.path.basename(image_path)
        image_url = f"{BASE_URL}/outputs/{filename}"

    # Optional logo URL (if user has a logo)
    logo_url = None
    if username:
        lp = load_logo_path(username)
        if lp:
            logo_filename = os.path.basename(lp)
            logo_url = f"{BASE_URL}/users/{username}/{logo_filename}"

   
    return {
        "generated_image": image_path,         # local path for server-side use
        "generated_image_url": image_url,      # URL for frontend <img/>
        "caption": caption,
        "timeline": timeline,
        "logo_url": logo_url,
    }


# --------------------------------------------------------------------------
# IMMEDIATE PUBLISH (Option 1)
# --------------------------------------------------------------------------

@app.post("/workflow/publish")
async def workflow_publish(
    username: str = Form(...),
    image_path: str = Form(...),
    caption_json: str = Form(...),
):
    """
    Immediate publish for interactive flow:
    - username: to look up insta creds
    - image_path: LOCAL path returned by /run_workflow (not the URL)
    - caption_json: JSON string of the caption dict from /run_workflow
    """
    try:
        profile = fetch_full_profile(username)
    except Exception as e:
        raise HTTPException(404, str(e))

    try:
        caption_data = json.loads(caption_json)
    except Exception:
        caption_data = caption_json  # fallback

    publish_to_instagram(
        profile["insta_id"],
        profile["insta_pw"],
        caption_data,
        "outputs/" + image_path,
    )

    return {"status": "published", "username": username}


# --------------------------------------------------------------------------
# SCHEDULER ENDPOINTS (Option 2)
# --------------------------------------------------------------------------

@app.post("/scheduler/create")
async def scheduler_create(
    username: str = Form(...),
    festival_name: str = Form(...),
    festival_date: str = Form(...),   # ISO date or datetime
    extra_prompt: str = Form(""),     # optional extra creative brief
):
    """
    Create a scheduled campaign task.
    A cron job should call /scheduler/run_due periodically to execute due tasks.
    """
    try:
        ensure_user_exists(username)
    except Exception as e:
        raise HTTPException(404, str(e))

    try:
        task = create_task(username, festival_name, festival_date, extra_prompt)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {"status": "scheduled", "task": task}


@app.get("/scheduler/run_due")
async def scheduler_run_due(request: Request):
    """
    Called periodically by cron (Google Cloud Scheduler / Render Cron, etc.).
    - Finds tasks with status 'pending' and run_at <= now
    - Runs workflow for each
    - Emails user for approval using publisher.send_approval_email
    """

    # Optional security: shared secret for cron
    cron_secret = os.environ.get("CRON_SECRET")
    if cron_secret:
        header_secret = request.headers.get("X-Cron-Secret")
        if header_secret != cron_secret:
            raise HTTPException(status_code=403, detail="Forbidden: invalid cron secret")

    now = datetime.utcnow()
    due_tasks = get_due_tasks(now)
    processed = []

    sender_email = os.environ.get("SENDER_EMAIL")
    sender_app_password = os.environ.get("SENDER_APP_PASSWORD")
    if not sender_email or not sender_app_password:
        raise HTTPException(
            500, "SENDER_EMAIL and SENDER_APP_PASSWORD env vars must be set"
        )

    for task in due_tasks:
        username = task["username"]
        festival_name = task["festival_name"]
        festival_date = task["festival_date"]
        extra_prompt = task.get("extra_prompt", "")

        try:
            profile = fetch_full_profile(username)
        except Exception:
            # Skip if user missing
            task["status"] = "aborted"
            task["last_run_at"] = now.isoformat()
            save_task(task)
            continue

        # Build campaign prompt
        brand_details = profile["brand_details"]
        brand_idea = profile.get("brand_idea", "")

        user_prompt = (
            f"{brand_details}\n\n"
            f"Brand Idea: {brand_idea}\n\n"
            f"Campaign brief: Create an Instagram post for the festival '{festival_name}'. "
            f"The event date is {festival_date}.\n\n"
        )
        if extra_prompt:
            user_prompt += f"Additional creative guidance: {extra_prompt}\n"

        logo_path = profile.get("logo")
        context = {}
        if logo_path:
            context["logo_path"] = logo_path

        # Run workflow (non-stream use; timeline ignored here)
        result = run_workflow(user_prompt, context=context)

        caption_data = result.get("caption")
        image_path = result.get("generated_image")
        final_image_path = "outputs/" + image_path

        task["last_result"] = {
            "user_prompt": user_prompt,
            "caption": caption_data,
            # "image_path": image_path,
            "image_path": final_image_path,
        }
        task["generation_count"] = task.get("generation_count", 0) + 1
        task["status"] = "generated"
        task["last_run_at"] = now.isoformat()
        save_task(task)

        # Compose and send approval email
        campaign_data = {
            "caption": caption_data,
            "image_path": final_image_path,
            "sender_email": sender_email,
            "sender_app_password": sender_app_password,
            "festival_name": festival_name,
        }

        try:
            send_approval_email(task["task_id"], profile["gmail"], campaign_data)
        except Exception as e:
            # Email failure doesn't change the generation result, but we log it
            print(f"Error sending approval email for task {task['task_id']}: {e}")

        processed.append(task["task_id"])

    return {
        "status": "ok",
        "now": now.isoformat(),
        "processed_tasks": processed,
    }


from fastapi.responses import HTMLResponse

@app.api_route("/scheduler/publish/{task_id}", methods=["GET", "POST"])
async def scheduler_publish(task_id: str, request: Request):
    """
    User clicked 'Publish' from email for a scheduled campaign.
    """
    try:
        task = load_task(task_id)
    except Exception as e:
        raise HTTPException(404, str(e))

    username = task["username"]
    try:
        profile = fetch_full_profile(username)
    except Exception as e:
        raise HTTPException(404, str(e))

    last_result = task.get("last_result")
    if not last_result:
        raise HTTPException(400, "No generated result found for this task.")

    caption_data = last_result.get("caption")
    image_path = last_result.get("image_path")

    publish_to_instagram(
        profile["insta_id"],
        profile["insta_pw"],
        caption_data,
        image_path,
    )

    task["status"] = "published"
    save_task(task)

    # 🌟 NEW: If accessed via browser (GET), return a clean HTML page
    if request.method == "GET":
        return HTMLResponse("""
            <html>
              <body style="font-family: Arial; padding: 40px; text-align: center">
                <h1>✅ Campaign Published</h1>
                <p>Your post has been successfully published to Instagram.</p>
              </body>
            </html>
        """)

    # Original JSON for POST (untouched)
    return {"status": "published", "task_id": task_id}


@app.api_route("/scheduler/regenerate/{task_id}", methods=["GET", "POST"])
async def scheduler_regenerate(task_id: str):
    """
    User clicked 'Regenerate' from email.
    - Re-runs workflow
    - Updates task.last_result
    - Sends another email
    """
    try:
        task = load_task(task_id)
    except Exception as e:
        raise HTTPException(404, str(e))

    username = task["username"]
    festival_name = task["festival_name"]
    festival_date = task["festival_date"]
    extra_prompt = task.get("extra_prompt", "")

    try:
        profile = fetch_full_profile(username)
    except Exception as e:
        raise HTTPException(404, str(e))

    sender_email = os.environ.get("SENDER_EMAIL")
    sender_app_password = os.environ.get("SENDER_APP_PASSWORD")
    if not sender_email or not sender_app_password:
        raise HTTPException(
            500, "SENDER_EMAIL and SENDER_APP_PASSWORD env vars must be set"
        )

    # Build campaign prompt again
    brand_details = profile["brand_details"]
    brand_idea = profile.get("brand_idea", "")

    user_prompt = (
        f"{brand_details}\n\n"
        f"Brand Idea: {brand_idea}\n\n"
        f"Campaign brief: Create an Instagram post for the festival '{festival_name}'. "
        f"The event date is {festival_date}.\n\n"
    )
    if extra_prompt:
        user_prompt += f"Additional creative guidance: {extra_prompt}\n"

    logo_path = profile.get("logo")
    context = {}
    if logo_path:
        context["logo_path"] = logo_path

    result = run_workflow(user_prompt, context=context)

    caption_data = result.get("caption")
    image_path = result.get("generated_image")

    now = datetime.utcnow()

    task["last_result"] = {
        "user_prompt": user_prompt,
        "caption": caption_data,
        "image_path": image_path,
    }
    task["generation_count"] = task.get("generation_count", 0) + 1
    task["status"] = "generated"
    task["last_run_at"] = now.isoformat()
    save_task(task)

    # Send another approval email
    campaign_data = {
        "caption": caption_data,
        "image_path": image_path,
        "sender_email": sender_email,
        "sender_app_password": sender_app_password,
        "festival_name": festival_name,
    }

    try:
        send_approval_email(task["task_id"], profile["gmail"], campaign_data)
    except Exception as e:
        print(f"Error sending approval email for task {task['task_id']} (regen): {e}")

    return {"status": "regenerated", "task_id": task_id}


@app.api_route("/scheduler/abort/{task_id}", methods=["GET", "POST"])
async def scheduler_abort(task_id: str):
    """
    User clicked 'Abort' from email.
    """
    try:
        task = load_task(task_id)
    except Exception as e:
        raise HTTPException(404, str(e))

    task["status"] = "aborted"
    save_task(task)

    return {"status": "aborted", "task_id": task_id}
