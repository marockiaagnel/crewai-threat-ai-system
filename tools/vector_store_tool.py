from crewai.tools import BaseTool
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from pydantic import PrivateAttr
import os

class VectorStoreTool(BaseTool):
    name: str = "VectorStoreTool"
    description: str = "Stores and queries structured logs in ChromaDB vector DB"

    # Private attributes (Pydantic won't validate these)
    _client: PersistentClient = PrivateAttr()
    _collection = PrivateAttr()
    _model: SentenceTransformer = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        persist_dir = os.getenv("CHROMA_DIR", "./chromadb")
        self._client = PersistentClient(path=persist_dir)
        self._collection = self._client.get_or_create_collection(name="threat_logs")
        self._model = SentenceTransformer("all-MiniLM-L6-v2")

    def _run(self, documents: list):
        texts = [str(d) for d in documents]
        embeddings = self._model.encode(texts).tolist()
        ids = [f"log_{i}" for i in range(len(texts))]

        self._collection.add(documents=texts, embeddings=embeddings, ids=ids)
        return {"status": "embedded", "count": len(texts)}

    def query(self, query_text: str, top_k=3):
        query_embedding = self._model.encode([query_text]).tolist()[0]
        results = self._collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return results["documents"][0] if results["documents"] else []
