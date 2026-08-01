from fastapi import FastAPI

from src.services.rag_service import RagService
from src.api.schemas import QueryRequest, QueryResponse


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


@app.post("/ingest")
def ingest():

    return rag_service.ingest()


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    answer = rag_service.query(request.question)

    return QueryResponse(
        question=request.question,
        answer=answer
    )