from fastapi import FastAPI
import os
import time
from datetime import datetime

app = FastAPI()

DATA_DIR = "/data"
COUNTER_FILE = os.path.join(DATA_DIR, "counter.txt")
LOGS_FILE = os.path.join(DATA_DIR, "logs.txt")
START_TIME = time.time()

# Ensure logs file exists
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except OSError:
        pass  # Fallback for read-only systems or permission issues if simulated

if not os.path.exists(LOGS_FILE):
    try:
        with open(LOGS_FILE, "w") as f:
            f.write(f"[{datetime.now()}] System initialized.\n")
    except:
        pass


def log_event(event: str):
    try:
        with open(LOGS_FILE, "a") as f:
            f.write(f"[{datetime.now()}] {event}\n")
    except:
        pass


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


@app.get("/api/logs")
def get_logs():
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r") as f:
                lines = f.readlines()
                return {"logs": [line.strip() for line in lines[-10:]]}
        except:
            return {"logs": []}
    return {"logs": []}


@app.get("/api/healthcheck")
def healthcheck(token: str = None):
    # Simple Auth Check (Demo)
    if token == "secret123":
        auth_status = "authenticated"
    else:
        auth_status = "public"

    # 1. Check persistence
    persistence_status = False
    try:
        test_file = os.path.join(DATA_DIR, "health_test.tmp")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        persistence_status = True
    except:
        persistence_status = False

    # 2. Check Latency (simulated)
    start = time.time()
    _ = 1 + 1
    latency = (time.time() - start) * 1000  # ms

    return {
        "status": "healthy" if persistence_status else "unhealthy",
        "persistence": "writable" if persistence_status else "readonly",
        "latency_ms": round(latency, 2),
        "cloud_run": "yes" if os.environ.get("K_SERVICE") else "no",
        "auth": auth_status,
    }


@app.get("/api/config")
def get_config():
    # Return safe environment variables
    return {
        "APP_VERSION": os.environ.get("APP_VERSION", "dev"),
        "APP_ENV": os.environ.get("APP_ENV", "local"),
        "SERVICE_NAME": os.environ.get("K_SERVICE", "local-container"),
    }


@app.get("/api/metrics")
def get_metrics():
    # Helper for charts
    uptime = int(get_uptime())

    # Get visit count safely
    count = 0
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r") as f:
                val = f.read().strip()
                if val.isdigit():
                    count = int(val)
        except:
            pass

    return {"total_visits": count, "uptime_seconds": uptime, "version": "1.0.0"}


@app.post("/api/rollback")
def simulate_rollback():
    log_event("Rollback simulated: Version 1.0.0 restored.")
    return {"status": "rollback_initiated", "target_version": "1.0.0-prev"}


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


from pydantic import BaseModel
import json


class VisitData(BaseModel):
    name: str


VISITS_FILE = os.path.join(DATA_DIR, "visitas.json")


@app.post("/api/visit")
def register_visit(data: VisitData):
    entry = {"name": data.name, "timestamp": datetime.now().isoformat()}

    visits = []
    if os.path.exists(VISITS_FILE):
        try:
            with open(VISITS_FILE, "r") as f:
                visits = json.load(f)
        except:
            pass

    visits.append(entry)

    # Keep only last 10 visits for demo purposes
    if len(visits) > 10:
        visits = visits[-10:]

    try:
        with open(VISITS_FILE, "w") as f:
            json.dump(visits, f, indent=2)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "success", "saved_entry": entry, "total_stored": len(visits)}


@app.get("/api/visits")
def get_visits():
    if os.path.exists(VISITS_FILE):
        try:
            with open(VISITS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []
