from elasticsearch import Elasticsearch
import os
import time
import requests

def wait_for_es(url, timeout=60):
    """Wait until Elasticsearch is ready before returning the client."""
    for i in range(timeout):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print("✅ Elasticsearch is ready!")
                # Add request_timeout here so every ES call has more time
                return Elasticsearch(url, request_timeout=60)
        except Exception:
            pass
        print(f"⏳ Waiting for Elasticsearch... ({i+1}/{timeout})")
        time.sleep(1)
    raise RuntimeError("❌ Elasticsearch not available after timeout")

# Initialize ES client
es_url = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
es = wait_for_es(es_url)

def log_to_elasticsearch(index, stage, data):
    """
    Logs a dictionary or list of dictionaries into Elasticsearch.
    Automatically adds the 'stage' field to each document.
    """
    if isinstance(data, list):
        for entry in data:
            entry["stage"] = stage
            es.index(index=index, document=entry)
    else:
        data["stage"] = stage
        es.index(index=index, document=data)
