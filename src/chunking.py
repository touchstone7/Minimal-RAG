from dataclasses import dataclass

from documents import Document


@dataclass
class Chunk:
    document_name: str
    text: str


def chunk_documents(
    documents: list[Document],
    chunk_size: int,
    overlap: int
) -> list[Chunk]:
    """
    Split documents into overlapping character-based chunks.

    Args:
        documents: List of loaded documents.
        chunk_size: Maximum characters in one chunk.
        overlap: Number of overlapping characters.

    Returns:
        List of Chunk objects.
    """

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[Chunk] = []

    step = chunk_size - overlap

    for document in documents:

        text = document.content

        for start in range(0, len(text), step):

            end = start + chunk_size

            chunk_text = text[start:end]

            if not chunk_text:
                break

            chunks.append(
                Chunk(
                    document_name=document.filename,
                    text=chunk_text
                )
            )

            if end >= len(text):
                break

    return chunks