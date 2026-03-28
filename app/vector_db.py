from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
import os
from typing import List, Dict, Any

load_dotenv()

class QdrantManager:
    def __init__(self, collection_name: str = os.getenv("QDRANT_COLLECTION")):
        self.client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
        self.collection_name = collection_name

    def create_collection(self, vector_size: int):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

    def upsert(self, embedded_chunks: List[Dict[str, Any]], batch_size: int = 100):
        for i in range(0, len(embedded_chunks), batch_size):
            batch = embedded_chunks[i:i+batch_size]

            points = [
                PointStruct(
                    id = chunk["id"],
                    vector = chunk["embedding"].tolist(),
                    payload = { "text": chunk["text"], **chunk["metadata"] }
                ) for chunk in batch
            ]

            self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query: List[float], top_k: int = 5):
        results = self.client.query_points(
            collection_name = self.collection_name,
            query = query,
            limit = top_k,
        )
        return results

    def collection_exist(self) -> bool:
        collections = self.client.get_collections().collections
        return any(collection.name == self.collection_name for collection in collections)