from documents import load_documents
from chunking import chunk_documents


def main():

    documents = load_documents("data")

    chunks = chunk_documents(
        documents=documents,
        chunk_size=50,
        overlap=10
    )

    print(f"Created {len(chunks)} chunk(s)\n")

    for index, chunk in enumerate(chunks, start=1):

        print(f"Chunk {index}")
        print(f"Document : {chunk.document_name}")
        print("-" * 40)
        print(chunk.text)
        print()


if __name__ == "__main__":
    main()