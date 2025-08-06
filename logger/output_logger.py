import json
from datetime import datetime
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_to_json(stage, data):
    timestamp = datetime.utcnow().isoformat()
    log_data = {
        "timestamp": timestamp,
        "stage": stage,
        "data": data
    }
    with open(os.path.join(LOG_DIR, f"{stage}.log"), "a") as f:
        f.write(json.dumps(log_data) + "\n")