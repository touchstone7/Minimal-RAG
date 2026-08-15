from src.models import Chunk, Document


def chunk_documents(
    documents: list[Document],
    chunk_size: int,
    overlap: int
) -> list[Chunk]:
    """
    Split documents into overlapping character-based chunks.
    """

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    chunks: list[Chunk] = []

    step = chunk_size - overlap

    for document in documents:

        text = document.content

        chunk_index = 0

        for start in range(0, len(text), step):

            end = start + chunk_size

            chunk_text = text[start:end]

            if not chunk_text:
                break

            chunks.append(
                Chunk(
                    document_id=document.document_id,
                    filename=document.filename,
                    chunk_index=chunk_index,
                    text=chunk_text
                )
            )

            chunk_index += 1

            if end >= len(text):
                break

    return chunks