from fastapi import FastAPI
import os
import time
from datetime import datetime

app = FastAPI()

DATA_DIR = "/data"
COUNTER_FILE = os.path.join(DATA_DIR, "counter.txt")
START_TIME = time.time()


def get_uptime():
    return time.time() - START_TIME


def increment_counter():
    count = 0
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
        except OSError:
            # Fallback for read-only systems or permission issues if simulated
            pass

    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r") as f:
                content = f.read().strip()
                if content.isdigit():
                    count = int(content)
        except Exception:
            pass

    count += 1

    try:
        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))
    except Exception:
        # Avoid crashing if volume is not writable
        pass

    return count


@app.get("/api/health")
def read_health():
    return {"status": "ok"}


@app.get("/api/status")
def read_status():
    uptime_seconds = int(get_uptime())
    visit_count = increment_counter()
    return {
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "uptime": f"{uptime_seconds}s",
        "visit_count": visit_count,
        "env": os.getenv("APP_ENV", "development"),
    }
