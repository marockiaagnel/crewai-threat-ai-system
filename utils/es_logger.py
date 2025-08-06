from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch("http://localhost:9200")

def log_to_elasticsearch(index, document):
    doc = {
        "timestamp": datetime.utcnow().isoformat(),
        **document
    }
    es.index(index=index, document=doc)