import ollama

from src.config import EMBEDDING_MODEL

from src.models import (
    Chunk,
    EmbeddedChunk,
)


# =========================================================
# EMBED CHUNKS
# =========================================================

def embed_chunks(
    chunks: list[Chunk],
    model: str = EMBEDDING_MODEL
) -> list[EmbeddedChunk]:
    """
    Generate embeddings for all chunks.
    """

    embedded_chunks: list[EmbeddedChunk] = []

    for chunk in chunks:

        response = ollama.embed(
            model=model,
            input=chunk.text
        )

        embedding = response["embeddings"][0]

        embedded_chunks.append(
            EmbeddedChunk(
                document_id=chunk.document_id,

                filename=chunk.filename,

                chunk_index=chunk.chunk_index,

                text=chunk.text,

                embedding=embedding
            )
        )

    return embedded_chunks


# =========================================================
# EMBED QUERY
# =========================================================

def embed_query(
    question: str,
    model: str = EMBEDDING_MODEL
) -> list[float]:
    """
    Generate an embedding for a user query.
    """

    response = ollama.embed(
        model=model,
        input=question
    )

    return response["embeddings"][0]