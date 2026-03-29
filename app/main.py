from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
# from app.app import search_query
from pathlib import Path

app = FastAPI()
path = Path(__file__).resolve().parent.parent
INDEX_URL = path / "static" / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://multi-modal-rag-system-rpli.onrender.com/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse(INDEX_URL)

# @app.get("/search")
# async def search(query: str):
#     result = search_query(query)
#     return {
#         "answer": " ".join(result[:2]),
#         "results": [{"text": r} for r in result]
#     }