import hashlib

import chromadb

from src.config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
)

from src.models import EmbeddedChunk


def create_collection():

    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def _generate_chunk_id(
    chunk: EmbeddedChunk
) -> str:

    raw_id = (
        f"{chunk.filename}:"
        f"{chunk.chunk_index}"
    )

    return hashlib.sha256(
        raw_id.encode("utf-8")
    ).hexdigest()


def index_chunks(
    collection,
    chunks: list[EmbeddedChunk]
):

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:

        ids.append(
            _generate_chunk_id(chunk)
        )

        documents.append(
            chunk.text
        )

        embeddings.append(
            chunk.embedding
        )

        metadatas.append(
            {
                "document": chunk.filename,
                "chunk_index": chunk.chunk_index,
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def show_collection_info(collection):

    print(
        f"Collection contains "
        f"{collection.count()} chunk(s)"
    )


def inspect_collection(collection):

    result = collection.get()

    print(result)