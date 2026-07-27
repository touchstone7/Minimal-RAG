from documents import load_documents
from chunking import chunk_documents
from embeddings import embed_chunks
from vectordb import create_collection, index_chunks


def main():

    documents = load_documents("data")

    chunks = chunk_documents(
        documents=documents,
        chunk_size=50,
        overlap=10
    )

    embedded_chunks = embed_chunks(chunks)

    collection = create_collection()

    index_chunks(collection, embedded_chunks)

    print(f"Stored {len(embedded_chunks)} chunks inside ChromaDB")


if __name__ == "__main__":
    main()