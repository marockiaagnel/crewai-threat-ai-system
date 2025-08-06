from crewai.tools import BaseTool
from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class VectorStoreTool(BaseTool):
    name: str = "VectorStoreTool"
    description: str = "Stores and queries structured logs in ChromaDB vector DB"

    def __init__(self):
        # Create Chroma client with in-memory DB
        self.client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chromadb"))
        self.collection = self.client.get_or_create_collection(name="threat_logs")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def _run(self, documents: list):
        texts = [str(d) for d in documents]
        embeddings = self.model.encode(texts)
        ids = [f"log_{i}" for i in range(len(texts))]

        # Chroma expects flat list of strings + embeddings
        self.collection.add(documents=texts, embeddings=embeddings, ids=ids)

        return {"status": "embedded", "count": len(texts)}

    def query(self, query_text: str, top_k=3):
        query_embedding = self.model.encode([query_text])[0]
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return results["documents"][0] if results["documents"] else []