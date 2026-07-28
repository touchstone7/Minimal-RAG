from config import (
    CHUNK_SIZE,
    OVERLAP,
    SENTENCES_PER_CHUNK,
)

from chunkers.character_chunker import chunk_documents
from chunkers.sentence_chunker import sentence_chunk_documents


class CharacterChunker:

    def chunk(self, documents):

        return chunk_documents(
            documents,
            chunk_size=CHUNK_SIZE,
            overlap=OVERLAP,
        )


class SentenceChunker:

    def chunk(self, documents):

        return sentence_chunk_documents(
            documents,
            sentences_per_chunk=SENTENCES_PER_CHUNK,
        )


def get_chunker(method: str):

    if method == "character":
        return CharacterChunker()

    if method == "sentence":
        return SentenceChunker()

    raise ValueError(
        f"Unknown chunking method: {method}"
    )