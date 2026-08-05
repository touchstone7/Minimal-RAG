from fastapi import FastAPI, UploadFile, File

from src.services.rag_service import RagService
from src.api.schemas import (
    QueryRequest,
    QueryResponse,
    IngestResponse,
)

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Minimal RAG API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

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


# =========================================================
# RAG SERVICE
# =========================================================

rag_service = RagService()


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "running"
    }


# =========================================================
# INGEST DOCUMENT
# =========================================================
@app.post(
    "/ingest",
    response_model=IngestResponse
)
async def ingest(
    file: UploadFile = File(...)
):

    return await rag_service.ingest_file(file)


# =========================================================
# QUERY
# =========================================================

@app.post(
    "/query",
    response_model=QueryResponse
)
def query(request: QueryRequest):

    answer = rag_service.query(
        request.question
    )

    return QueryResponse(
        question=request.question,
        answer=answer
    )