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
        f"{chunk.document_id}:"
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
                "document_id": str(
                    chunk.document_id
                ),
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

    result = collection.get(
        include=[
            "documents",
            "metadatas",
        ]
    )

    ids = result["ids"]
    documents = result["documents"]
    metadatas = result["metadatas"]

    print("\n========== CHROMA COLLECTION ==========\n")

    for index, chroma_id in enumerate(ids):

        metadata = metadatas[index]
        document = documents[index]

        print(f"Record #{index}")
        print(f"Chroma ID: {chroma_id}")
        print(
            f"Document ID: "
            f"{metadata.get('document_id', 'OLD / NOT PRESENT')}"
        )
        print(
            f"Filename: "
            f"{metadata.get('document', 'UNKNOWN')}"
        )
        print(
            f"Chunk Index: "
            f"{metadata.get('chunk_index', 'OLD / NOT PRESENT')}"
        )
        print(
            f"Text: "
            f"{document[:100]}..."
        )
        print("--------------------------------------")

    print(
        f"\nTotal records: {len(ids)}"
    )

    print(
        "\n======================================\n"
    )