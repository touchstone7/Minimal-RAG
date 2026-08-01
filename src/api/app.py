from fastapi import FastAPI

from src.services.rag_service import RagService

app = FastAPI(
    title="Minimal RAG API",
    version="1.0.0"
)

rag_service = RagService()


@app.get("/health")
def health():

    return {
        "status": "running"
    }