import re

from src.models import Chunk, Document

def sentence_chunk_documents(documents, sentences_per_chunk=2):

    chunks = []

    for document in documents:

        sentences = re.split(
            r'(?<=[.!?])\s+',
            document.content.strip()
        )

        for i in range(0, len(sentences), sentences_per_chunk):

            chunk_text = " ".join(
                sentences[i:i + sentences_per_chunk]
            )

            chunks.append(
                Chunk(
                    filename=document.filename,
                    text=chunk_text
                )
            )

    return chunks