import ollama

from src.models import Chunk, EmbeddedChunk


def embed_chunks(
    chunks: list[Chunk],
    model: str = "nomic-embed-text"
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