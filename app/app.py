from app.data import DocumentLoader
from app.embedding import EmbeddingPipeline
from app.vector_db import QdrantManager

pipeline = EmbeddingPipeline()
db = QdrantManager()

def upload_data(path: str = "./data"):
    # if not db.collection_exist():
    loader = DocumentLoader(path)
    data = loader.load()
    embedded_data = pipeline.process(data)
    vector_size = len(embedded_data[0]["embedding"])
    db.create_collection(vector_size)
    db.upsert(embedded_data)

def search_query(query_text: str = "What is DL?"):
    query = pipeline.model.encode([query_text], normalize_embeddings=True, show_progress_bar=False)[0]
    results = db.search(query.tolist(), top_k=5)

    result = []
    for point in (p for _, pts in results for p in pts):
        result.append(point.payload.get("text", ""))

    return result