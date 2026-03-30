from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np
import hashlib
import uuid

class EmbeddingPipeline:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100, model_name: str = "all-MiniLM-L6-v2", batch_size: int = 64, normalize: bool = True):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n", " ", ""])
        self.model = SentenceTransformer(model_name, device="cpu")
        self.batch_size = batch_size
        self.normalize = normalize

    def chunk_documents(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = []

        for doc in docs:
            content = doc.get("content", "")

            if not content or not isinstance(content, str):
                continue

            splits = self.splitter.split_text(content)
            total_chunks = len(splits)
            
            for i, chunk in enumerate(splits):
                if not chunk.strip():
                    continue

                chunk_id = str(uuid.uuid4())
                chunks.append({
                    "id": chunk_id,
                    "text": chunk,
                    "metadata": {
                        **doc.get("metadata", {}),
                        "chunk_index": i,
                        "total_chunks": total_chunks
                    },
                    "parent_hash": doc["hash"],
                    "chunk_hash": self._hash_text(chunk)
                })

        return chunks

    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(texts, batch_size=self.batch_size, normalize_embeddings=self.normalize, show_progress_bar=True)
        enriched = []
        for chunk, emb in zip(chunks, embeddings):
            enriched.append({
                **chunk,
                "embedding": np.array(emb, dtype="float32")
            })

        return enriched

    def process(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = self.chunk_documents(docs)
        embedded = self.embed_chunks(chunks)
        return embedded

    def _hash_text(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()