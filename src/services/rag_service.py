from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

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

from src.llm.llm_factory import get_llm_provider


class RagService:

    def __init__(self):
        """
        Initialize the RAG service.

        Connect to the persistent ChromaDB collection immediately.

        The LLM is provided through an abstraction so RagService
        does not depend directly on Ollama, Gemini, or any other
        specific provider.
        """

        # ----------------------------------------------------------
        # Connect to persistent ChromaDB collection
        # ----------------------------------------------------------

        self.collection = create_collection()

        # ----------------------------------------------------------
        # Initialize configured LLM provider
        # ----------------------------------------------------------

        self.llm_provider = get_llm_provider()

        print(
            f"\nRAG service initialized."
        )

        print(
            f"Existing knowledge base contains "
            f"{self.collection.count()} chunk(s)."
        )

        print(
            f"LLM provider: "
            f"{LLM_PROVIDER}\n"
        )


    def ingest(self):

        # ==========================================================
        # FULL INGESTION
        #
        # Loads every supported document currently present inside
        # DATA_DIRECTORY.
        #
        # Used for initial population / rebuilding of the knowledge
        # base.
        # ==========================================================

        # ----------------------------
        # Step 1: Load documents
        # ----------------------------

        documents = load_documents(
            DATA_DIRECTORY
        )

        # ----------------------------
        # Step 2: Chunk documents
        # ----------------------------

        chunker = get_chunker(
            CHUNKING_METHOD
        )

        chunks = chunker.chunk(
            documents
        )

        print(
            f"\nCreated {len(chunks)} chunk(s)\n"
        )

        if not chunks:

            return {
                "status": "success",
                "chunks_created": 0,
                "total_chunks": self.collection.count(),
            }

        # ----------------------------
        # Step 3: Generate embeddings
        # ----------------------------

        embedded_chunks = embed_chunks(
            chunks
        )

        # ----------------------------
        # Step 4: Store embeddings
        # ----------------------------

        index_chunks(
            self.collection,
            embedded_chunks
        )

        # ----------------------------
        # Step 5: Verify storage
        # ----------------------------

        show_collection_info(
            self.collection
        )

        return {
            "status": "success",
            "chunks_created": len(chunks),
            "total_chunks": self.collection.count(),
        }


    async def ingest_file(
        self,
        file: UploadFile
    ):

        # ==========================================================
        # INCREMENTAL FILE INGESTION
        #
        # Upload one new document
        #       ↓
        # Generate unique document ID
        #       ↓
        # Save file to data/
        #       ↓
        # Load ONLY that document
        #       ↓
        # Attach document ID
        #       ↓
        # Chunk ONLY that document
        #       ↓
        # Embed ONLY that document
        #       ↓
        # Add chunks to existing collection
        #
        # The document ID is independent of the filename.
        #
        # Therefore two different uploads named "paper.pdf"
        # can coexist logically in the vector database.
        # ==========================================================

        # ==========================================================
        # STEP 1: Validate filename
        # ==========================================================

        if not file.filename:

            raise ValueError(
                "Uploaded file must have a filename."
            )

        filename = Path(
            file.filename
        ).name

        extension = Path(
            filename
        ).suffix.lower()

        supported_extensions = {
            ".txt",
            ".md",
            ".pdf",
            ".docx",
        }

        if extension not in supported_extensions:

            raise ValueError(
                f"Unsupported file type: {extension}. "
                f"Supported formats: "
                f"{', '.join(sorted(supported_extensions))}"
            )

        # ==========================================================
        # STEP 2: Generate a unique document ID
        # ==========================================================

        document_id = uuid4()

        # ==========================================================
        # STEP 3: Save file into data/
        # ==========================================================

        data_directory = Path(
            DATA_DIRECTORY
        )

        data_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = data_directory / filename

        contents = await file.read()

        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(
                contents
            )

        # ==========================================================
        # STEP 4: Load ONLY the uploaded document
        # ==========================================================
        #
        # The loader creates a Document object containing the
        # document content and filename.
        #
        # We explicitly replace its generated ID with the ID
        # belonging to THIS upload.
        #
        # This keeps the ingestion operation deterministic:
        #
        # upload
        #   ↓
        # document_id
        #   ↓
        # chunks
        #   ↓
        # chunk IDs
        #
        # Filename is metadata, not identity.
        # ==========================================================

        documents = load_documents(
            DATA_DIRECTORY
        )

        uploaded_document = [
            document
            for document in documents
            if document.filename == filename
        ]

        if not uploaded_document:

            raise ValueError(
                f"Could not load uploaded document: {filename}"
            )

        document = uploaded_document[0]

        document.document_id = document_id

        # ==========================================================
        # STEP 5: Chunk ONLY this document
        # ==========================================================

        chunker = get_chunker(
            CHUNKING_METHOD
        )

        chunks = chunker.chunk(
            [document]
        )

        chunks_added = len(chunks)

        if chunks_added == 0:

            raise ValueError(
                f"No chunks were created from {filename}."
            )

        # ==========================================================
        # STEP 6: Generate embeddings
        # ==========================================================

        embedded_chunks = embed_chunks(
            chunks
        )

        # ==========================================================
        # STEP 7: Add ONLY new chunks to existing collection
        # ==========================================================

        index_chunks(
            self.collection,
            embedded_chunks
        )

        # ==========================================================
        # STEP 8: Get updated collection size
        # ==========================================================

        total_chunks = self.collection.count()

        print(
            f"\nAdded {chunks_added} chunk(s) "
            f"from {filename}"
        )

        print(
            f"Document ID: "
            f"{document_id}"
        )

        print(
            f"Collection now contains "
            f"{total_chunks} chunk(s)\n"
        )

        return {
            "status": "success",
            "document_id": str(document_id),
            "filename": filename,
            "chunks_added": chunks_added,
            "total_chunks": total_chunks,
        }


    def query(
        self,
        question: str
    ):

        # ==========================================================
        # RETRIEVAL PIPELINE
        #
        # User Question
        #      ↓
        # Vector Search
        #      ↓
        # Prompt Construction
        #      ↓
        # LLM Provider
        #      ↓
        # Final Answer
        # ==========================================================

        # ----------------------------------------------------------
        # Safety check
        # ----------------------------------------------------------

        if self.collection.count() == 0:

            raise ValueError(
                "Knowledge base is empty. "
                "Ingest at least one document before querying."
            )

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
        # Step 3: Generate final answer
        # ----------------------------

        return self.llm_provider.generate(
            prompt
        )