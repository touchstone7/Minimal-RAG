from documents import load_documents
from chunking import chunk_documents
from embeddings import embed_chunks


def main():

    documents = load_documents("data")

    chunks = chunk_documents(
        documents=documents,
        chunk_size=50,
        overlap=10
    )

    embedded_chunks = embed_chunks(chunks)

    print(f"Generated embeddings for {len(embedded_chunks)} chunk(s)\n")

    for index, chunk in enumerate(embedded_chunks, start=1):

        print(f"Chunk {index}")
        print(f"Document : {chunk.document_name}")

        print("-" * 40)

        print(chunk.text)

        print()

        print(f"Embedding Dimension : {len(chunk.embedding)}")

        print("First 10 Values:")

        print(chunk.embedding[:10])

        print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()