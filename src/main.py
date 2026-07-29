from loaders.loader_factory import load_documents

from chunkers.chunker_factory import get_chunker

from embeddings import embed_chunks

from vectordb import (
    create_collection,
    index_chunks,
    show_collection_info,
)

from retriever import retrieve
from prompt_builder import build_prompt
from llm import ask_llm

from config import (
    DATA_DIRECTORY,
    CHUNKING_METHOD,
)

def main():

    # ----------------------------
    # Step 1: Load documents
    # ----------------------------
    documents = load_documents(DATA_DIRECTORY)

    # ----------------------------
    # Step 2: Chunk documents
    # ----------------------------
    chunker = get_chunker(CHUNKING_METHOD)

    chunks = chunker.chunk(documents)
    print(f"\nCreated {len(chunks)} chunk(s)\n")

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
    # Step 9: Build prompt
    # ----------------------------
    prompt = build_prompt(
        question=question,
        retrieved_chunks=retrieved_chunks,
    )

    # Uncomment to inspect the prompt sent to the LLM
    #
    # print("\nGenerated Prompt\n")
    # print(prompt)

    # ----------------------------
    # Step 10: Ask the LLM
    # ----------------------------
    answer = ask_llm(prompt)

    # ----------------------------
    # Step 11: Display answer
    # ----------------------------
    print("\nAnswer")
    print("=" * 60)
    print(answer)
    print("=" * 60)


if __name__ == "__main__":
    main()