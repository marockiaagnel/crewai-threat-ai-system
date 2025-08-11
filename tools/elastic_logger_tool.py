from crewai.tools import BaseTool
from elasticsearch import Elasticsearch
from pydantic import PrivateAttr
import os

class ElasticLoggerTool(BaseTool):
    name: str = "ElasticLoggerTool"
    description: str = "Logs structured data into Elasticsearch for dashboarding"

    # Private attribute (excluded from Pydantic validation/serialization)
    _client: Elasticsearch = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = Elasticsearch(os.getenv("ES_HOST", "http://localhost:9200"))

    def _run(self, data: dict):
        index_name = "threat-ai-logs"
        response = self._client.index(index=index_name, document=data)
        return {"status": "logged", "id": response.get("_id")}