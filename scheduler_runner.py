# scheduler_runner.py
import time
import requests

API = "http://localhost:8000/scheduler/run_due"

print("🟢 Local Scheduler Started (checking every 60 sec)\n")

while True:
    try:
        r = requests.get(API, timeout=10)
        print("⏱️ Checked →", r.text[:200])
    except Exception as e:
        print("❌ Scheduler error:", e)

    time.sleep(60)
