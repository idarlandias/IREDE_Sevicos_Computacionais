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
