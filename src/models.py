from dataclasses import dataclass
from uuid import UUID


@dataclass
class Document:
    document_id: UUID
    filename: str
    content: str


@dataclass
class Chunk:
    document_id: UUID
    filename: str
    chunk_index: int
    text: str


@dataclass
class EmbeddedChunk:
    document_id: UUID
    filename: str
    chunk_index: int
    text: str
    embedding: list[float]

@dataclass
class RetrievedChunk:
    document_id: UUID
    filename: str
    chunk_index: int
    text: str

    score: float
    rank: int

    vector_store: str
    collection_name: str

    point_id: str