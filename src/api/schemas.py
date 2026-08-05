from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str


class IngestResponse(BaseModel):
    status: str
    filename: str
    chunks_added: int
    total_chunks: int