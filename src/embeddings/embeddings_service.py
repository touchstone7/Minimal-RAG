
import ollama

from src.models import Chunk, EmbeddedChunk


def embed_chunks(
    chunks: list[Chunk],
    model: str = "nomic-embed-text"
) -> list[EmbeddedChunk]:
    """
    Generate embeddings for all chunks.

    Args:
        chunks: List of Chunk objects.
        model: Ollama embedding model.

    Returns:
        List of EmbeddedChunk objects.
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
                filename=chunk.filename,
                text=chunk.text,
                embedding=embedding
            )
        )

    return embedded_chunks