# scheduler_utils.py

import os
import json
from datetime import datetime, timedelta
import uuid

SCHEDULED_DIR = "scheduled"
os.makedirs(SCHEDULED_DIR, exist_ok=True)


def _task_path(task_id: str) -> str:
    return os.path.join(SCHEDULED_DIR, f"{task_id}.json")


def create_task(username: str, festival_name: str, festival_date_iso: str, extra_prompt: str = "") -> dict:
    """
    Create a scheduled task file that will be picked up by /scheduler/run_due.
    festival_date_iso: ISO string like '2025-10-23T00:00:00' or '2025-10-23'
    """
    try:
        # Try parsing with time, then fallback to date
        try:
            festival_dt = datetime.fromisoformat(festival_date_iso)
        except ValueError:
            festival_dt = datetime.fromisoformat(festival_date_iso + "T00:00:00")
    except Exception as e:
        raise ValueError(f"Invalid festival_date format: {festival_date_iso}") from e

    # 48 hours before
    run_at = festival_dt - timedelta(hours=48)

    task_id = f"{username}_{festival_name}_{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()

    task = {
        "task_id": task_id,
        "username": username,
        "festival_name": festival_name,
        "festival_date": festival_dt.isoformat(),
        "run_at": run_at.isoformat(),
        "extra_prompt": extra_prompt or "",
        "status": "pending",  # pending -> generated -> published|aborted
        "generation_count": 0,
        "last_result": None,
        "created_at": now,
        "last_run_at": None,
    }

    with open(_task_path(task_id), "w") as f:
        json.dump(task, f, indent=2)

    return task


def load_task(task_id: str) -> dict:
    path = _task_path(task_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Task '{task_id}' not found.")
    with open(path) as f:
        return json.load(f)


def save_task(task: dict):
    task_id = task["task_id"]
    with open(_task_path(task_id), "w") as f:
        json.dump(task, f, indent=2)


def list_tasks() -> list:
    tasks = []
    for fname in os.listdir(SCHEDULED_DIR):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(SCHEDULED_DIR, fname)) as f:
            tasks.append(json.load(f))
    return tasks


def get_due_tasks(now: datetime | None = None) -> list:
    """
    Return tasks where status == 'pending' and now >= run_at.
    """
    if now is None:
        now = datetime.utcnow()
    tasks = list_tasks()
    due = []
    for t in tasks:
        if t.get("status") != "pending":
            continue
        run_at_str = t.get("run_at")
        if not run_at_str:
            continue
        try:
            run_at = datetime.fromisoformat(run_at_str)
        except Exception:
            continue
        if now >= run_at:
            due.append(t)
    return due
