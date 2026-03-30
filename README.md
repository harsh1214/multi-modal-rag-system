# 🧠 Multi-Modal RAG System

A production-ready Retrieval-Augmented Generation (RAG) system built with FastAPI, Qdrant, and Sentence Transformers.

## 🚀 Features
- Document ingestion pipeline (offline)
- Smart chunking & embedding
- Qdrant vector database integration
- Fast semantic search API
- Lightweight frontend (HTML + Tailwind)
- Lazy model loading for deployment efficiency

## 🏗️ Architecture

Offline (Ingestion)
Documents → Chunk → Embed → Qdrant Cloud

Online (Query)
User Query → Embed → Search Qdrant → Return Results

## 📁 Project Structure

app/
├── main.py
├── app.py
├── data.py
├── embedding.py
├── vector_db.py

static/
└── index.html

requirements.txt

## ⚙️ Setup

1. Clone repo
2. Create virtual environment
3. Install dependencies

## 🔐 Environment Variables

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_api_key
QDRANT_COLLECTION=your_collection_name

## ▶️ Run API

uvicorn app.main:app --reload

## 🔍 API

GET /search?query=your_query

## 🚧 Notes

- Do NOT run ingestion in API
- Use Qdrant Cloud
- Lazy loading required for deployment