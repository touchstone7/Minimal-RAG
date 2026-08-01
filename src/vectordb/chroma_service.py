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


def index_chunks(collection, chunks: list[EmbeddedChunk]):

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(str(index))

        documents.append(chunk.text)

        embeddings.append(chunk.embedding)

        metadatas.append(
            {
                "document": chunk.filename
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def show_collection_info(collection):

    print(f"Collection contains {collection.count()} chunk(s)")


def inspect_collection(collection):

    result = collection.get()

    print(result)