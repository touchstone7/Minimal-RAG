import chromadb

from embeddings import EmbeddedChunk


def create_collection(name: str = "minimal-rag"):

    client = chromadb.Client()

    try:
        client.delete_collection(name)
    except Exception:
        pass

    return client.create_collection(name)


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
                "document": chunk.document_name
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )