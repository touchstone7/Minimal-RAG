from dataclasses import dataclass


@dataclass
class Document:
    filename: str
    content: str


@dataclass
class Chunk:
    filename: str
    chunk_index: int
    text: str


@dataclass
class EmbeddedChunk:
    filename: str
    chunk_index: int
    text: str
    embedding: list[float]