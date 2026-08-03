from fastapi import FastAPI

from src.services.rag_service import RagService
from src.api.schemas import QueryRequest, QueryResponse

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Minimal RAG API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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