import re

from src.models import Chunk, Document


def sentence_chunk_documents(
    documents: list[Document],
    sentences_per_chunk: int = 2
):

    chunks: list[Chunk] = []

    for document in documents:

        sentences = re.split(
            r'(?<=[.!?])\s+',
            document.content.strip()
        )

        chunk_index = 0

        for i in range(
            0,
            len(sentences),
            sentences_per_chunk
        ):

            chunk_text = " ".join(
                sentences[
                    i:i + sentences_per_chunk
                ]
            )

            chunks.append(
                Chunk(
                    document_id=document.document_id,
                    filename=document.filename,
                    chunk_index=chunk_index,
                    text=chunk_text
                )
            )

            chunk_index += 1

    return chunks