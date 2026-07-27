from documents import load_documents
from chunking import (
    chunk_documents,
    sentence_chunk_documents
)
from embeddings import embed_chunks
from vectordb import (
    create_collection,
    index_chunks,
    show_collection_info,
)
from retriever import retrieve
from prompt_builder import build_prompt
from llm import ask_llm


def main():

    # ----------------------------
    # Step 1: Load documents
    # ----------------------------
    documents = load_documents("data")

    # ----------------------------
    # Step 2: Chunk documents
    # ----------------------------
    # Character chunking
    # chunks = chunk_documents(
    #     documents,
    #     chunk_size=50,
    #     overlap=10,
    # )

    # Sentence chunking
    chunks = sentence_chunk_documents(
        documents,
        sentences_per_chunk=2
    )

    print(f"\nCreated {len(chunks)} chunks\n")

    for i, chunk in enumerate(chunks):

        print("=" * 60)
        print(f"Chunk {i + 1}")
        print(f"Document : {chunk.filename}")
        print("-" * 60)
        print(chunk.text)

    # ----------------------------
    # Step 3: Generate embeddings
    # ----------------------------
    embedded_chunks = embed_chunks(chunks)

    # ----------------------------
    # Step 4: Create Chroma collection
    # ----------------------------
    collection = create_collection()

    # ----------------------------
    # Step 5: Store embeddings
    # ----------------------------
    index_chunks(collection, embedded_chunks)

    # ----------------------------
    # Step 6: Verify storage
    # ----------------------------
    show_collection_info(collection)

    # ----------------------------
    # Step 7: Ask user for a question
    # ----------------------------
    question = input("\nAsk a question: ")

    # ----------------------------
    # Step 8: Retrieve relevant chunks
    # ----------------------------
    retrieved_chunks = retrieve(
        collection=collection,
        question=question,
    )

    # ----------------------------
    # Step 9: Build the prompt
    # ----------------------------
    prompt = build_prompt(
        question=question,
        retrieved_chunks=retrieved_chunks,
    )

    # Uncomment this if you want to see exactly
    # what is being sent to the LLM.
    #
    # print("\nGenerated Prompt\n")
    # print(prompt)

    # ----------------------------
    # Step 10: Ask the LLM
    # ----------------------------
    answer = ask_llm(prompt)

    # ----------------------------
    # Step 11: Display the answer
    # ----------------------------
    print("\nAnswer")
    print("=" * 60)
    print(answer)
    print("=" * 60)


if __name__ == "__main__":
    main()