from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from src.config import (
    DATA_DIRECTORY,
    CHUNKING_METHOD,
    TOP_K,
    LLM_PROVIDER,
)

from src.loaders.loader_factory import (
    load_document
)

from src.chunkers.chunker_factory import (
    get_chunker
)

from src.embeddings.embeddings_service import (
    embed_chunks
)

from src.vectordb.vector_store_factory import (
    get_vector_store
)

from src.retrieval.retriever import (
    retrieve
)

from src.retrieval.prompt_builder import (
    build_prompt
)

from src.llm.llm_factory import (
    get_llm_provider
)


class RagService:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):

        # -----------------------------------------------------
        # Vector store
        # -----------------------------------------------------

        self.vector_store = (
            get_vector_store()
        )

        # -----------------------------------------------------
        # LLM provider
        # -----------------------------------------------------

        self.llm_provider = (
            get_llm_provider()
        )

        # -----------------------------------------------------
        # Service information
        # -----------------------------------------------------

        print(
            "\nRAG service initialized."
        )

        print(
            f"Existing knowledge base contains "
            f"{self.vector_store.count()} "
            f"chunk(s)."
        )

        print(
            f"Vector store: "
            f"{self.vector_store.info()['vector_store']}"
        )

        print(
            f"LLM provider: "
            f"{LLM_PROVIDER}\n"
        )

    # =========================================================
    # INGEST FILE
    # =========================================================

    async def ingest_file(
        self,
        file: UploadFile
    ):

        # =====================================================
        # STEP 1: VALIDATE FILENAME
        # =====================================================

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

        # =====================================================
        # STEP 2: GENERATE DOCUMENT ID
        # =====================================================

        document_id = uuid4()

        # =====================================================
        # STEP 3: SAVE FILE
        # =====================================================

        data_directory = Path(
            DATA_DIRECTORY
        )

        data_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = (
            data_directory / filename
        )

        contents = await file.read()

        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(
                contents
            )

        # =====================================================
        # STEP 4: LOAD DOCUMENT
        # =====================================================

        document = load_document(
            file_path=file_path,
            document_id=document_id
        )

        if document is None:

            raise ValueError(
                f"Could not load uploaded document: "
                f"{filename}"
            )

        # =====================================================
        # STEP 5: CHUNK DOCUMENT
        # =====================================================

        chunker = get_chunker(
            CHUNKING_METHOD
        )

        chunks = chunker.chunk(
            [document]
        )

        chunks_added = len(chunks)

        if chunks_added == 0:

            raise ValueError(
                f"No chunks were created from "
                f"{filename}."
            )

        # =====================================================
        # STEP 6: GENERATE EMBEDDINGS
        # =====================================================

        embedded_chunks = embed_chunks(
            chunks
        )

        # =====================================================
        # STEP 7: INDEX INTO VECTOR STORE
        # =====================================================

        self.vector_store.index(
            embedded_chunks
        )

        # =====================================================
        # STEP 8: GET UPDATED COUNT
        # =====================================================

        total_chunks = (
            self.vector_store.count()
        )

        # =====================================================
        # LOGGING
        # =====================================================

        print(
            f"\nAdded {chunks_added} chunk(s) "
            f"from {filename}"
        )

        print(
            f"Document ID: "
            f"{document_id}"
        )

        print(
            f"Vector store now contains "
            f"{total_chunks} chunk(s)\n"
        )

        return {
            "status": "success",

            "document_id": str(
                document_id
            ),

            "filename": filename,

            "chunks_added": chunks_added,

            "total_chunks": total_chunks,
        }

    # =========================================================
    # QUERY
    # =========================================================

    def query(
        self,
        question: str
    ):

        # =====================================================
        # SAFETY CHECK
        # =====================================================

        if self.vector_store.count() == 0:

            raise ValueError(
                "Knowledge base is empty. "
                "Ingest at least one document "
                "before querying."
            )

        # =====================================================
        # STEP 1: RETRIEVE
        # =====================================================

        retrieved_chunks = retrieve(
            vector_store=self.vector_store,

            question=question,

            top_k=TOP_K,
        )

        # =====================================================
        # STEP 2: BUILD PROMPT
        # =====================================================

        prompt = build_prompt(
            question=question,

            retrieved_chunks=retrieved_chunks,
        )

        # =====================================================
        # STEP 3: GENERATE ANSWER
        # =====================================================

        return self.llm_provider.generate(
            prompt
        )

    # =========================================================
    # VECTOR STORE INFO
    # =========================================================

    def vector_store_info(self) -> dict:

        return self.vector_store.info()

    # =========================================================
    # VECTOR STORE INSPECTION
    # =========================================================

    def inspect_vector_store(
        self,
        limit: int = 10
    ) -> list[dict]:

        return self.vector_store.inspect(
            limit=limit
        )