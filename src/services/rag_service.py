from src.config import *

from src.loaders.loader_factory import load_documents
from src.chunkers.chunker_factory import get_chunker

from src.embeddings.embeddings_service import embed_chunks

from src.vectordb.chroma_service import (
    create_collection,
    index_chunks,
    show_collection_info,
)

from src.retrieval.retriever import retrieve
from src.retrieval.prompt_builder import build_prompt

from src.llm.ollama_service import ask_llm


class RagService:

    def __init__(self):
        """
        Initialize the RAG service.

        The vector database collection is created during the
        ingestion phase and reused for all subsequent queries.
        """

        self.collection = None

    def ingest(self):

        # ==========================================================
        # INGESTION PIPELINE
        #
        # Converts raw documents into a searchable knowledge base.
        #
        # Documents
        #      ↓
        # Chunking
        #      ↓
        # Embeddings
        #      ↓
        # ChromaDB
        # ==========================================================

        # ----------------------------
        # Step 1: Load all documents
        # ----------------------------
        documents = load_documents(DATA_DIRECTORY)

        # ----------------------------
        # Step 2: Split documents into chunks
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
        # Step 3: Convert chunks into vector embeddings
        # ----------------------------
        embedded_chunks = embed_chunks(chunks)

        # ----------------------------
        # Step 4: Create/Open the vector database
        # ----------------------------
        self.collection = create_collection()

        # ----------------------------
        # Step 5: Store embeddings in ChromaDB
        # ----------------------------
        index_chunks(
            self.collection,
            embedded_chunks
        )

        # ----------------------------
        # Step 6: Verify indexed chunks
        # ----------------------------
        show_collection_info(self.collection)

    def query(self, question: str):

        # ==========================================================
        # RETRIEVAL PIPELINE
        #
        # User Question
        #      ↓
        # Vector Search
        #      ↓
        # Prompt Construction
        #      ↓
        # LLM
        #      ↓
        # Final Answer
        # ==========================================================

        # ----------------------------
        # Step 1: Retrieve relevant chunks
        # ----------------------------
        retrieved_chunks = retrieve(
            collection=self.collection,
            question=question,
        )

        # ----------------------------
        # Step 2: Build the LLM prompt
        # ----------------------------
        prompt = build_prompt(
            question=question,
            retrieved_chunks=retrieved_chunks,
        )

        # ----------------------------
        # Step 3: Generate the final answer
        # ----------------------------
        return ask_llm(prompt)