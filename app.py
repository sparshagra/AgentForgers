# # # # # from fastapi import FastAPI, File, Form, UploadFile
# # # # # from fastapi.responses import JSONResponse
# # # # # from main import run_workflow
# # # # # import os
# # # # # import json

# # # # # app = FastAPI()

# # # # # UPLOAD_DIR = "uploads"
# # # # # os.makedirs(UPLOAD_DIR, exist_ok=True)

# # # # # @app.post("/run_workflow")
# # # # # async def run_workflow_endpoint(
# # # # #     user_prompt: str = Form(...),
# # # # #     logo: UploadFile = File(None),
# # # # #     context: str = Form("{}")
# # # # # ):
# # # # #     logo_path = None
# # # # #     if logo:
# # # # #         filename = logo.filename
# # # # #         file_location = os.path.join(UPLOAD_DIR, filename)
# # # # #         with open(file_location, "wb") as f:
# # # # #             # Handle file in chunks for safety
# # # # #             while content := await logo.read(1024 * 1024):
# # # # #                 f.write(content)
# # # # #         logo_path = file_location

# # # # #     # Safely parse context
# # # # #     try:
# # # # #         user_context = json.loads(context)
# # # # #         if not isinstance(user_context, dict):
# # # # #             raise ValueError()
# # # # #     except Exception:
# # # # #         return JSONResponse(
# # # # #             status_code=400,
# # # # #             content={"error": "Invalid context JSON. Must be a valid JSON object."}
# # # # #         )

# # # # #     # Add logo file path to user context (used by your workflow)
# # # # #     if logo_path:
# # # # #         user_context["logo_path"] = logo_path

# # # # #     result = run_workflow(user_prompt, context=user_context)
# # # # #     ig_post = result.get("ig_post") if isinstance(result, dict) else None
# # # # #     return {
# # # # #         **result,
# # # # #         "ig_post": ig_post
# # # # #     }

# # # # from fastapi import FastAPI, File, Form, UploadFile
# # # # from fastapi.responses import JSONResponse
# # # # from main import run_workflow
# # # # import os
# # # # import json

# # # # app = FastAPI()

# # # # UPLOAD_DIR = "uploads"
# # # # os.makedirs(UPLOAD_DIR, exist_ok=True)

# # # # @app.post("/run_workflow")
# # # # async def run_workflow_endpoint(
# # # #     user_prompt: str = Form(...),
# # # #     logo: UploadFile = File(None),
# # # #     context: str = Form("{}")
# # # # ):
# # # #     logo_path = None
# # # #     if logo:
# # # #         filename = logo.filename
# # # #         file_location = os.path.join(UPLOAD_DIR, filename)
# # # #         with open(file_location, "wb") as f:
# # # #             # Handle file in chunks for safety
# # # #             while content := await logo.read(1024 * 1024):
# # # #                 f.write(content)
# # # #         logo_path = file_location

# # # #     # Safely parse context
# # # #     try:
# # # #         user_context = json.loads(context)
# # # #         if not isinstance(user_context, dict):
# # # #             raise ValueError()
# # # #     except Exception:
# # # #         return JSONResponse(
# # # #             status_code=400,
# # # #             content={"error": "Invalid context JSON. Must be a valid JSON object."}
# # # #         )

# # # #     # Add logo file path to user context (used by your workflow)
# # # #     if logo_path:
# # # #         user_context["logo_path"] = logo_path

# # # #     result = run_workflow(user_prompt, context=user_context)

# # # #     # ✅ As requested: FastAPI returns ONLY generated image + caption output
# # # #     return {
# # # #         "generated_image": result.get("generated_image"),
# # # #         "caption": result.get("caption"),
# # # #     }

# # # from fastapi import FastAPI, File, Form, UploadFile
# # # from fastapi.responses import JSONResponse, StreamingResponse
# # # from main import run_workflow
# # # from orchestrator import stream_workflow
# # # import os
# # # import json

# # # app = FastAPI()

# # # UPLOAD_DIR = "uploads"
# # # os.makedirs(UPLOAD_DIR, exist_ok=True)

# # # @app.post("/run_workflow")
# # # async def run_workflow_endpoint(
# # #     user_prompt: str = Form(...),
# # #     logo: UploadFile = File(None),
# # #     context: str = Form("{}")
# # # ):
# # #     logo_path = None
# # #     if logo:
# # #         filename = logo.filename
# # #         file_location = os.path.join(UPLOAD_DIR, filename)
# # #         with open(file_location, "wb") as f:
# # #             # Handle file in chunks for safety
# # #             while content := await logo.read(1024 * 1024):
# # #                 f.write(content)
# # #         logo_path = file_location

# # #     # Safely parse context
# # #     try:
# # #         user_context = json.loads(context)
# # #         if not isinstance(user_context, dict):
# # #             raise ValueError()
# # #     except Exception:
# # #         return JSONResponse(
# # #             status_code=400,
# # #             content={"error": "Invalid context JSON. Must be a valid JSON object."}
# # #         )

# # #     # Add logo file path to user context (used by your workflow)
# # #     if logo_path:
# # #         user_context["logo_path"] = logo_path

# # #     result = run_workflow(user_prompt, context=user_context)

# # #     # ✅ As requested: FastAPI returns ONLY generated image + caption output
# # #     return {
# # #         "generated_image": result.get("generated_image"),
# # #         "caption": result.get("caption"),
# # #     }


# # # @app.post("/run_workflow_stream")
# # # async def run_workflow_stream_endpoint(
# # #     user_prompt: str = Form(...),
# # #     logo: UploadFile = File(None),
# # #     context: str = Form("{}")
# # # ):
# # #     """
# # #     SSE endpoint that streams the workflow progress step-by-step.

# # #     Frontend can connect and show a timeline:
# # #     - WriterAgent → Outliner → Captioner → Designer → ImageGenerator → FINAL
# # #     """

# # #     logo_path = None
# # #     if logo:
# # #         filename = logo.filename
# # #         file_location = os.path.join(UPLOAD_DIR, filename)
# # #         with open(file_location, "wb") as f:
# # #             while content := await logo.read(1024 * 1024):
# # #                 f.write(content)
# # #         logo_path = file_location

# # #     # Safely parse context
# # #     try:
# # #         user_context = json.loads(context)
# # #         if not isinstance(user_context, dict):
# # #             raise ValueError()
# # #     except Exception:
# # #         return JSONResponse(
# # #             status_code=400,
# # #             content={"error": "Invalid context JSON. Must be a valid JSON object."}
# # #         )

# # #     if logo_path:
# # #         user_context["logo_path"] = logo_path

# # #     def event_generator():
# # #         """
# # #         Synchronous generator used by StreamingResponse.
# # #         It wraps orchestrator.stream_workflow and converts
# # #         each LangGraph event into an SSE 'data: {...}\n\n' payload.
# # #         """
# # #         last_state = None

# # #         try:
# # #             for raw_event in stream_workflow(user_prompt, context=user_context):
# # #                 # raw_event is expected to be a mapping like { "AgentName": {state...} }
# # #                 if not isinstance(raw_event, dict):
# # #                     continue

# # #                 for node_name, node_state in raw_event.items():
# # #                     # Skip non-agent keys if any appear (like system events)
# # #                     if not isinstance(node_state, dict):
# # #                         continue

# # #                     # Track last_state so we can send a final summary at the end
# # #                     last_state = node_state

# # #                     # Build a compact payload for the frontend timeline
# # #                     payload = {
# # #                         "step": node_name,
# # #                     }

# # #                     # Optionally include key fields when present
# # #                     for key in [
# # #                         "enhanced",
# # #                         "outline",
# # #                         "caption",
# # #                         "image_prompt",
# # #                         "generated_image",
# # #                         "compliance_blocked",
# # #                         "compliance_stage",
# # #                         "compliance_reason",
# # #                     ]:
# # #                         if key in node_state:
# # #                             payload[key] = node_state[key]

# # #                     # Serialize to JSON safely
# # #                     try:
# # #                         data_str = json.dumps(payload, ensure_ascii=False, default=str)
# # #                     except Exception as e:
# # #                         # Fallback minimal error payload
# # #                         data_str = json.dumps({
# # #                             "step": node_name,
# # #                             "error": f"Serialization error: {e}"
# # #                         })

# # #                     # SSE event
# # #                     yield f"data: {data_str}\n\n"

# # #             # After streaming all nodes, send one FINAL summary event
# # #             if last_state is not None:
# # #                 final_payload = {
# # #                     "step": "FINAL",
# # #                     "generated_image": last_state.get("generated_image"),
# # #                     "caption": last_state.get("caption"),
# # #                 }
# # #                 try:
# # #                     final_str = json.dumps(final_payload, ensure_ascii=False, default=str)
# # #                 except Exception as e:
# # #                     final_str = json.dumps({
# # #                         "step": "FINAL",
# # #                         "error": f"Serialization error: {e}"
# # #                     })
# # #                 yield f"data: {final_str}\n\n"

# # #         except Exception as e:
# # #             # In case of unexpected error, send one error event
# # #             err_payload = {
# # #                 "step": "ERROR",
# # #                 "error": str(e),
# # #             }
# # #             err_str = json.dumps(err_payload, ensure_ascii=False, default=str)
# # #             yield f"data: {err_str}\n\n"

# # #     return StreamingResponse(event_generator(), media_type="text/event-stream")

# # from fastapi import FastAPI, File, Form, UploadFile, HTTPException
# # from fastapi.responses import JSONResponse, StreamingResponse

# # from user_utils import (
# #     ensure_unique_username,
# #     save_login, save_brand, save_logo,
# #     check_password, fetch_full_profile,
# #     ensure_user_exists, load_brand, load_logo_path
# # )

# # from main import run_workflow
# # from orchestrator import stream_workflow

# # import os
# # import json

# # app = FastAPI()

# # UPLOAD_DIR = "uploads"
# # os.makedirs(UPLOAD_DIR, exist_ok=True)

# # # --------------------------------------------------------------------------
# # # USER MANAGEMENT ENDPOINTS
# # # --------------------------------------------------------------------------

# # @app.post("/register")
# # async def register(
# #     username: str = Form(...),
# #     password: str = Form(...),
# #     gmail: str = Form(...),
# #     insta_id: str = Form(...),
# #     insta_pw: str = Form(...),
# #     brand_details: str = Form(...),
# #     brand_idea: str = Form(...),
# #     logo: UploadFile = File(...)
# # ):
# #     # Username MUST be unique
# #     try:
# #         ensure_unique_username(username)
# #     except ValueError:
# #         raise HTTPException(400, "Username already exists.")

# #     # Save login details
# #     save_login(username, password, gmail, insta_id, insta_pw)

# #     # Save brand details
# #     save_brand(username, brand_details, brand_idea)

# #     # Save logo
# #     logo_bytes = await logo.read()
# #     save_logo(username, logo_bytes)

# #     return {"status": "registered", "username": username}


# # @app.post("/login")
# # async def login(username: str = Form(...), password: str = Form(...)):
# #     try:
# #         ensure_user_exists(username)
# #     except FileNotFoundError:
# #         raise HTTPException(404, "User not found")

# #     if not check_password(username, password):
# #         raise HTTPException(401, "Invalid password")

# #     profile = fetch_full_profile(username)
# #     return {"status": "logged_in", "profile": profile}


# # @app.get("/user/{username}/profile")
# # async def get_profile(username: str):
# #     try:
# #         profile = fetch_full_profile(username)
# #     except Exception as e:
# #         raise HTTPException(404, str(e))
# #     return profile


# # @app.post("/user/update_brand")
# # async def update_brand(
# #     username: str = Form(...),
# #     brand_details: str = Form(None),
# #     brand_idea: str = Form(None),
# #     logo: UploadFile = File(None),
# # ):
# #     try:
# #         ensure_user_exists(username)
# #     except Exception as e:
# #         raise HTTPException(404, str(e))

# #     if brand_details or brand_idea:
# #         # load existing details
# #         existing = load_brand(username)
# #         save_brand(
# #             username,
# #             brand_details or existing["brand_details"],
# #             brand_idea or existing["brand_idea"],
# #         )

# #     logo_path = None
# #     if logo:
# #         bytes_data = await logo.read()
# #         logo_path = save_logo(username, bytes_data)

# #     return {
# #         "status": "brand_updated",
# #         "logo_updated": bool(logo),
# #         "logo_path": logo_path
# #     }


# # @app.get("/user/fetch")
# # async def fetch_user(username: str):
# #     try:
# #         return fetch_full_profile(username)
# #     except Exception as e:
# #         raise HTTPException(404, str(e))


# # # --------------------------------------------------------------------------
# # # WORKFLOW ENDPOINTS (Phase 1 + Phase 2)
# # # --------------------------------------------------------------------------

# # @app.post("/run_workflow")
# # async def run_workflow_endpoint(
# #     user_prompt: str = Form(...),
# #     username: str = Form(None),   # NEW: allow passing username instead of logo upload
# #     logo: UploadFile = File(None),
# #     context: str = Form("{}")
# # ):
# #     logo_path = None

# #     # If user is known → auto-load their logo
# #     if username:
# #         try:
# #             logo_path = load_logo_path(username)
# #         except:
# #             pass

# #     # If logo is uploaded, override the user’s stored logo
# #     if logo:
# #         filename = logo.filename
# #         file_location = os.path.join(UPLOAD_DIR, filename)
# #         with open(file_location, "wb") as f:
# #             while content := await logo.read(1024 * 1024):
# #                 f.write(content)
# #         logo_path = file_location

# #     # Parse context
# #     try:
# #         user_context = json.loads(context)
# #         if not isinstance(user_context, dict):
# #             raise ValueError()
# #     except:
# #         return JSONResponse(
# #             status_code=400,
# #             content={"error": "Invalid context JSON."}
# #         )

# #     if logo_path:
# #         user_context["logo_path"] = logo_path

# #     result = run_workflow(user_prompt, context=user_context)

# #     return {
# #         "generated_image": result.get("generated_image"),
# #         "caption": result.get("caption"),
# #     }


# # @app.post("/run_workflow_stream")
# # async def run_workflow_stream_endpoint(
# #     user_prompt: str = Form(...),
# #     username: str = Form(None),
# #     logo: UploadFile = File(None),
# #     context: str = Form("{}")
# # ):

# #     logo_path = None

# #     # Auto-load logo for user
# #     if username:
# #         try:
# #             logo_path = load_logo_path(username)
# #         except:
# #             pass

# #     if logo:
# #         filename = logo.filename
# #         file_path = os.path.join(UPLOAD_DIR, filename)
# #         with open(file_path, "wb") as f:
# #             while content := await logo.read(1024 * 1024):
# #                 f.write(content)
# #         logo_path = file_path

# #     try:
# #         user_context = json.loads(context)
# #         if not isinstance(user_context, dict):
# #             raise ValueError()
# #     except:
# #         return JSONResponse(
# #             status_code=400,
# #             content={"error": "Invalid context JSON."}
# #         )

# #     if logo_path:
# #         user_context["logo_path"] = logo_path

# #     def event_generator():
# #         last_state = None
# #         try:
# #             for raw_event in stream_workflow(user_prompt, context=user_context):
# #                 if not isinstance(raw_event, dict):
# #                     continue

# #                 for node, node_state in raw_event.items():
# #                     if not isinstance(node_state, dict):
# #                         continue

# #                     last_state = node_state

# #                     payload = {"step": node}
# #                     for key in ["enhanced", "outline", "caption", "image_prompt", "generated_image"]:
# #                         if key in node_state:
# #                             payload[key] = node_state[key]

# #                     yield "data: " + json.dumps(payload, ensure_ascii=False) + "\n\n"

# #             if last_state:
# #                 final_payload = {
# #                     "step": "FINAL",
# #                     "generated_image": last_state.get("generated_image"),
# #                     "caption": last_state.get("caption"),
# #                 }
# #                 yield "data: " + json.dumps(final_payload, ensure_ascii=False) + "\n\n"

# #         except Exception as e:
# #             err = {"step": "ERROR", "error": str(e)}
# #             yield "data: " + json.dumps(err) + "\n\n"

# #     return StreamingResponse(event_generator(), media_type="text/event-stream")

# from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request
# from fastapi.responses import JSONResponse, StreamingResponse

# from user_utils import (
#     ensure_unique_username,
#     save_login, save_brand, save_logo,
#     check_password, fetch_full_profile,
#     ensure_user_exists, load_brand, load_logo_path
# )

# from main import run_workflow
# from orchestrator import stream_workflow
# from scheduler_utils import (
#     create_task, get_due_tasks, load_task, save_task
# )
# from publisher import send_approval_email, publish_to_instagram

# import os
# import json
# from datetime import datetime

# app = FastAPI()

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # --------------------------------------------------------------------------
# # USER MANAGEMENT ENDPOINTS
# # --------------------------------------------------------------------------

# @app.post("/register")
# async def register(
#     username: str = Form(...),
#     password: str = Form(...),
#     gmail: str = Form(...),
#     insta_id: str = Form(...),
#     insta_pw: str = Form(...),
#     brand_details: str = Form(...),
#     brand_idea: str = Form(...),
#     logo: UploadFile = File(...)
# ):
#     # Username MUST be unique
#     try:
#         ensure_unique_username(username)
#     except ValueError:
#         raise HTTPException(400, "Username already exists.")

#     # Save login details
#     save_login(username, password, gmail, insta_id, insta_pw)

#     # Save brand details
#     save_brand(username, brand_details, brand_idea)

#     # Save logo
#     logo_bytes = await logo.read()
#     save_logo(username, logo_bytes)

#     return {"status": "registered", "username": username}


# @app.post("/login")
# async def login(username: str = Form(...), password: str = Form(...)):
#     try:
#         ensure_user_exists(username)
#     except FileNotFoundError:
#         raise HTTPException(404, "User not found")

#     if not check_password(username, password):
#         raise HTTPException(401, "Invalid password")

#     profile = fetch_full_profile(username)
#     return {"status": "logged_in", "profile": profile}


# @app.get("/user/{username}/profile")
# async def get_profile(username: str):
#     try:
#         profile = fetch_full_profile(username)
#     except Exception as e:
#         raise HTTPException(404, str(e))
#     return profile


# @app.post("/user/update_brand")
# async def update_brand(
#     username: str = Form(...),
#     brand_details: str = Form(None),
#     brand_idea: str = Form(None),
#     logo: UploadFile = File(None),
# ):
#     try:
#         ensure_user_exists(username)
#     except Exception as e:
#         raise HTTPException(404, str(e))

#     if brand_details or brand_idea:
#         # load existing details
#         existing = load_brand(username)
#         save_brand(
#             username,
#             brand_details or existing["brand_details"],
#             brand_idea or existing["brand_idea"],
#         )

#     logo_path = None
#     if logo:
#         bytes_data = await logo.read()
#         logo_path = save_logo(username, bytes_data)

#     return {
#         "status": "brand_updated",
#         "logo_updated": bool(logo),
#         "logo_path": logo_path
#     }


# @app.get("/user/fetch")
# async def fetch_user(username: str):
#     try:
#         return fetch_full_profile(username)
#     except Exception as e:
#         raise HTTPException(404, str(e))


# # --------------------------------------------------------------------------
# # WORKFLOW ENDPOINTS
# # --------------------------------------------------------------------------

# @app.post("/run_workflow")
# async def run_workflow_endpoint(
#     user_prompt: str = Form(...),
#     username: str = Form(None),   # allow passing username
#     logo: UploadFile = File(None),
#     context: str = Form("{}")
# ):
#     logo_path = None

#     # If user is known → auto-load their logo
#     if username:
#         try:
#             logo_path = load_logo_path(username)
#         except:
#             pass

#     # If logo is uploaded, override the user’s stored logo
#     if logo:
#         filename = logo.filename
#         file_location = os.path.join(UPLOAD_DIR, filename)
#         with open(file_location, "wb") as f:
#             while content := await logo.read(1024 * 1024):
#                 f.write(content)
#         logo_path = file_location

#     # Parse context
#     try:
#         user_context = json.loads(context)
#         if not isinstance(user_context, dict):
#             raise ValueError()
#     except:
#         return JSONResponse(
#             status_code=400,
#             content={"error": "Invalid context JSON."}
#         )

#     if logo_path:
#         user_context["logo_path"] = logo_path

#     result = run_workflow(user_prompt, context=user_context)

#     return {
#         "generated_image": result.get("generated_image"),
#         "caption": result.get("caption"),
#     }


# @app.post("/run_workflow_stream")
# async def run_workflow_stream_endpoint(
#     user_prompt: str = Form(...),
#     username: str = Form(None),
#     logo: UploadFile = File(None),
#     context: str = Form("{}")
# ):

#     logo_path = None

#     # Auto-load logo for user
#     if username:
#         try:
#             logo_path = load_logo_path(username)
#         except:
#             pass

#     if logo:
#         filename = logo.filename
#         file_path = os.path.join(UPLOAD_DIR, filename)
#         with open(file_path, "wb") as f:
#             while content := await logo.read(1024 * 1024):
#                 f.write(content)
#         logo_path = file_path

#     try:
#         user_context = json.loads(context)
#         if not isinstance(user_context, dict):
#             raise ValueError()
#     except:
#         return JSONResponse(
#             status_code=400,
#             content={"error": "Invalid context JSON."}
#         )

#     if logo_path:
#         user_context["logo_path"] = logo_path

#     def event_generator():
#         last_state = None
#         try:
#             for raw_event in stream_workflow(user_prompt, context=user_context):
#                 if not isinstance(raw_event, dict):
#                     continue

#                 for node, node_state in raw_event.items():
#                     if not isinstance(node_state, dict):
#                         continue

#                     last_state = node_state

#                     payload = {"step": node}
#                     for key in ["enhanced", "outline", "caption", "image_prompt", "generated_image"]:
#                         if key in node_state:
#                             payload[key] = node_state[key]

#                     yield "data: " + json.dumps(payload, ensure_ascii=False) + "\n\n"

#             if last_state:
#                 final_payload = {
#                     "step": "FINAL",
#                     "generated_image": last_state.get("generated_image"),
#                     "caption": last_state.get("caption"),
#                 }
#                 yield "data: " + json.dumps(final_payload, ensure_ascii=False) + "\n\n"

#         except Exception as e:
#             err = {"step": "ERROR", "error": str(e)}
#             yield "data: " + json.dumps(err) + "\n\n"

#     return StreamingResponse(event_generator(), media_type="text/event-stream")


# # --------------------------------------------------------------------------
# # IMMEDIATE PUBLISH (Option 1)
# # --------------------------------------------------------------------------

# @app.post("/workflow/publish")
# async def workflow_publish(
#     username: str = Form(...),
#     image_path: str = Form(...),
#     caption_json: str = Form(...)
# ):
#     """
#     Immediate publish for interactive flow:
#     - username: to look up insta creds
#     - image_path: path returned by /run_workflow
#     - caption_json: JSON string of the caption dict from /run_workflow
#     """
#     try:
#         profile = fetch_full_profile(username)
#     except Exception as e:
#         raise HTTPException(404, str(e))

#     try:
#         caption_data = json.loads(caption_json)
#     except Exception:
#         caption_data = caption_json  # fallback

#     publish_to_instagram(
#         profile["insta_id"],
#         profile["insta_pw"],
#         caption_data,
#         image_path
#     )

#     return {"status": "published", "username": username}


# # --------------------------------------------------------------------------
# # SCHEDULER ENDPOINTS (Option 2)
# # --------------------------------------------------------------------------

# @app.post("/scheduler/create")
# async def scheduler_create(
#     username: str = Form(...),
#     festival_name: str = Form(...),
#     festival_date: str = Form(...),   # ISO date or datetime
#     extra_prompt: str = Form("")      # optional extra creative brief
# ):
#     """
#     Create a scheduled campaign task. A Render Cron job should call /scheduler/run_due
#     periodically (e.g., hourly) to execute due tasks.
#     """
#     try:
#         ensure_user_exists(username)
#     except Exception as e:
#         raise HTTPException(404, str(e))

#     try:
#         task = create_task(username, festival_name, festival_date, extra_prompt)
#     except ValueError as e:
#         raise HTTPException(400, str(e))

#     return {"status": "scheduled", "task": task}


# @app.get("/scheduler/run_due")
# async def scheduler_run_due(request: Request):
#     """
#     Called periodically by Google Cloud Scheduler (HTTP target).
#     - Finds tasks with status 'pending' and run_at <= now
#     - Runs workflow for each
#     - Emails user for approval using publisher.send_approval_email

#     Security:
#     - If the environment variable CRON_SECRET is set, this endpoint expects
#       a matching 'X-Cron-Secret' header. This allows Cloud Scheduler to call
#       the endpoint securely while blocking random public calls.
#     """

#     # Optional security: shared secret for cron
#     cron_secret = os.environ.get("CRON_SECRET")
#     if cron_secret:
#         header_secret = request.headers.get("X-Cron-Secret")
#         if header_secret != cron_secret:
#             raise HTTPException(status_code=403, detail="Forbidden: invalid cron secret")

#     now = datetime.utcnow()
#     due_tasks = get_due_tasks(now)
#     processed = []

#     sender_email = os.environ.get("SENDER_EMAIL")
#     sender_app_password = os.environ.get("SENDER_APP_PASSWORD")
#     if not sender_email or not sender_app_password:
#         raise HTTPException(500, "SENDER_EMAIL and SENDER_APP_PASSWORD env vars must be set")

#     for task in due_tasks:
#         username = task["username"]
#         festival_name = task["festival_name"]
#         festival_date = task["festival_date"]
#         extra_prompt = task.get("extra_prompt", "")

#         try:
#             profile = fetch_full_profile(username)
#         except Exception as e:
#             # Skip if user missing
#             task["status"] = "aborted"
#             task["last_run_at"] = now.isoformat()
#             save_task(task)
#             continue

#         # Build campaign prompt
#         brand_details = profile["brand_details"]
#         brand_idea = profile.get("brand_idea", "")

#         user_prompt = (
#             f"{brand_details}\n\n"
#             f"Brand Idea: {brand_idea}\n\n"
#             f"Campaign brief: Create an Instagram post for the festival '{festival_name}'. "
#             f"The event date is {festival_date}.\n\n"
#         )
#         if extra_prompt:
#             user_prompt += f"Additional creative guidance: {extra_prompt}\n"

#         logo_path = profile.get("logo")
#         context = {}
#         if logo_path:
#             context["logo_path"] = logo_path

#         # Run workflow (non-stream)
#         result = run_workflow(user_prompt, context=context)

#         caption_data = result.get("caption")
#         image_path = result.get("generated_image")

#         task["last_result"] = {
#             "user_prompt": user_prompt,
#             "caption": caption_data,
#             "image_path": image_path,
#         }
#         task["generation_count"] = task.get("generation_count", 0) + 1
#         task["status"] = "generated"
#         task["last_run_at"] = now.isoformat()
#         save_task(task)

#         # Compose and send approval email
#         campaign_data = {
#             "caption": caption_data,
#             "image_path": image_path,
#             "sender_email": sender_email,
#             "sender_app_password": sender_app_password,
#             "festival_name": festival_name,
#         }

#         try:
#             send_approval_email(task["task_id"], profile["gmail"], campaign_data)
#         except Exception as e:
#             # Email failure doesn't change the generation result, but we log it
#             print(f"Error sending approval email for task {task['task_id']}: {e}")

#         processed.append(task["task_id"])

#     return {
#         "status": "ok",
#         "now": now.isoformat(),
#         "processed_tasks": processed,
#     }


# @app.post("/scheduler/publish/{task_id}")
# async def scheduler_publish(task_id: str):
#     """
#     User clicked 'Publish' from email for a scheduled campaign.
#     """
#     try:
#         task = load_task(task_id)
#     except Exception as e:
#         raise HTTPException(404, str(e))

#     username = task["username"]
#     try:
#         profile = fetch_full_profile(username)
#     except Exception as e:
#         raise HTTPException(404, str(e))

#     last_result = task.get("last_result")
#     if not last_result:
#         raise HTTPException(400, "No generated result found for this task.")

#     caption_data = last_result.get("caption")
#     image_path = last_result.get("image_path")

#     publish_to_instagram(
#         profile["insta_id"],
#         profile["insta_pw"],
#         caption_data,
#         image_path
#     )

#     task["status"] = "published"
#     save_task(task)

#     return {"status": "published", "task_id": task_id}


# @app.post("/scheduler/regenerate/{task_id}")
# async def scheduler_regenerate(task_id: str):
#     """
#     User clicked 'Regenerate' from email.
#     - Re-runs workflow
#     - Updates task.last_result
#     - Sends another email
#     """
#     try:
#         task = load_task(task_id)
#     except Exception as e:
#         raise HTTPException(404, str(e))

#     username = task["username"]
#     festival_name = task["festival_name"]
#     festival_date = task["festival_date"]
#     extra_prompt = task.get("extra_prompt", "")

#     try:
#         profile = fetch_full_profile(username)
#     except Exception as e:
#         raise HTTPException(404, str(e))

#     sender_email = os.environ.get("SENDER_EMAIL")
#     sender_app_password = os.environ.get("SENDER_APP_PASSWORD")
#     if not sender_email or not sender_app_password:
#         raise HTTPException(500, "SENDER_EMAIL and SENDER_APP_PASSWORD env vars must be set")

#     # Build campaign prompt again
#     brand_details = profile["brand_details"]
#     brand_idea = profile.get("brand_idea", "")

#     user_prompt = (
#         f"{brand_details}\n\n"
#         f"Brand Idea: {brand_idea}\n\n"
#         f"Campaign brief: Create an Instagram post for the festival '{festival_name}'. "
#         f"The event date is {festival_date}.\n\n"
#     )
#     if extra_prompt:
#         user_prompt += f"Additional creative guidance: {extra_prompt}\n"

#     logo_path = profile.get("logo")
#     context = {}
#     if logo_path:
#         context["logo_path"] = logo_path

#     result = run_workflow(user_prompt, context=context)

#     caption_data = result.get("caption")
#     image_path = result.get("generated_image")

#     now = datetime.utcnow()

#     task["last_result"] = {
#         "user_prompt": user_prompt,
#         "caption": caption_data,
#         "image_path": image_path,
#     }
#     task["generation_count"] = task.get("generation_count", 0) + 1
#     task["status"] = "generated"
#     task["last_run_at"] = now.isoformat()
#     save_task(task)

#     # Send another approval email
#     campaign_data = {
#         "caption": caption_data,
#         "image_path": image_path,
#         "sender_email": sender_email,
#         "sender_app_password": sender_app_password,
#         "festival_name": festival_name,
#     }

#     try:
#         send_approval_email(task["task_id"], profile["gmail"], campaign_data)
#     except Exception as e:
#         print(f"Error sending approval email for task {task['task_id']} (regen): {e}")

#     return {"status": "regenerated", "task_id": task_id}


# @app.post("/scheduler/abort/{task_id}")
# async def scheduler_abort(task_id: str):
#     """
#     User clicked 'Abort' from email.
#     """
#     try:
#         task = load_task(task_id)
#     except Exception as e:
#         raise HTTPException(404, str(e))

#     task["status"] = "aborted"
#     save_task(task)

#     return {"status": "aborted", "task_id": task_id}



from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse

from user_utils import (
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

from main import run_workflow
from scheduler_utils import (
    create_task,
    get_due_tasks,
    load_task,
    save_task,
)
from publisher import send_approval_email, publish_to_instagram

import os
import json
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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

    # Save logo
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

    # If user is known → auto-load their logo
    if username:
        try:
            logo_path = load_logo_path(username)
        except Exception:
            pass

    # If logo is uploaded, override the user’s stored logo
    if logo:
        filename = logo.filename
        file_location = os.path.join(UPLOAD_DIR, filename)
        with open(file_location, "wb") as f:
            while content := await logo.read(1024 * 1024):
                f.write(content)
        logo_path = file_location

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

    if logo_path:
        user_context["logo_path"] = logo_path

    result = run_workflow(user_prompt, context=user_context)

    # 🔁 Now also return the timeline (previously SSE)
    return {
        "generated_image": result.get("generated_image"),
        "caption": result.get("caption"),
        "timeline": result.get("timeline", []),
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
    - image_path: path returned by /run_workflow
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
        image_path,
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
        except Exception as e:
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

        task["last_result"] = {
            "user_prompt": user_prompt,
            "caption": caption_data,
            "image_path": image_path,
        }
        task["generation_count"] = task.get("generation_count", 0) + 1
        task["status"] = "generated"
        task["last_run_at"] = now.isoformat()
        save_task(task)

        # Compose and send approval email
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
            # Email failure doesn't change the generation result, but we log it
            print(f"Error sending approval email for task {task['task_id']}: {e}")

        processed.append(task["task_id"])

    return {
        "status": "ok",
        "now": now.isoformat(),
        "processed_tasks": processed,
    }


@app.post("/scheduler/publish/{task_id}")
async def scheduler_publish(task_id: str):
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

    return {"status": "published", "task_id": task_id}


@app.post("/scheduler/regenerate/{task_id}")
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


@app.post("/scheduler/abort/{task_id}")
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
