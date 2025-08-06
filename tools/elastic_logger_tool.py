from crewai.tools import BaseTool
from elasticsearch import Elasticsearch
import os

class ElasticLoggerTool(BaseTool):
    name: str = "ElasticLoggerTool"
    description: str = "Logs structured data into Elasticsearch for dashboarding"

    def __init__(self):
        self.client = Elasticsearch(os.getenv("ES_HOST", "http://localhost:9200"))

    def _run(self, data: dict):
        index_name = "threat-ai-logs"
        response = self.client.index(index=index_name, document=data)
        return {"status": "logged", "id": response.get("_id")}