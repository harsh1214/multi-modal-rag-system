# from app.data import DocumentLoader
from app.embedding import EmbeddingPipeline
from app.vector_db import QdrantManager

pipeline = None
db = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        pipeline = EmbeddingPipeline()
    return pipeline

def get_db():
    global db
    if db is None:
        db = QdrantManager()
    return db

# def upload_data(path: str = "./data"):
#     print("Loading documents...")
#     loader = DocumentLoader(path)
#     docs = loader.load()

#     print("Embedding...")
#     pipeline = EmbeddingPipeline()
#     embedded = pipeline.process(docs)

#     print("Uploading to Qdrant...")
#     db = QdrantManager()

#     vector_size = len(embedded[0]["embedding"])

#     if not db.collection_exist():
#         db.create_collection(vector_size)

#     db.upsert(embedded)

def search_query(query_text: str = "What is DL?"):
    pipeline = get_pipeline()
    db = get_db()

    query = pipeline.model.encode([query_text], normalize_embeddings=True, show_progress_bar=False)[0]
    results = db.search(query.tolist(), top_k=3)

    result = []
    for point in (p for _, pts in results for p in pts):
        result.append(point.payload.get("text", ""))

    return result