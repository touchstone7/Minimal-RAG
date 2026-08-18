import hashlib

from uuid import UUID

import chromadb

from src.config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
)

from src.models import (
    EmbeddedChunk,
    RetrievedChunk,
)

from src.vectordb.vector_store import VectorStore


class ChromaVectorStore(VectorStore):

    # =========================================================
    # CONSTRUCTOR
    # =========================================================

    def __init__(self):

        self.client = None
        self.collection = None

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def initialize(self) -> None:

        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME,

                metadata={
                    "hnsw:space": "cosine"
                }
            )
        )

    # =========================================================
    # POINT ID
    # =========================================================

    @staticmethod
    def _generate_chunk_id(
        chunk: EmbeddedChunk
    ) -> str:

        raw_id = (
            f"{chunk.document_id}:"
            f"{chunk.chunk_index}"
        )

        return hashlib.sha256(
            raw_id.encode("utf-8")
        ).hexdigest()

    # =========================================================
    # INDEX
    # =========================================================

    def index(
        self,
        chunks: list[EmbeddedChunk]
    ) -> None:

        if not chunks:
            return

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:

            ids.append(
                self._generate_chunk_id(chunk)
            )

            documents.append(
                chunk.text
            )

            embeddings.append(
                chunk.embedding
            )

            metadatas.append(
                {
                    "document_id": str(
                        chunk.document_id
                    ),

                    "filename": chunk.filename,

                    "chunk_index": chunk.chunk_index,
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def search(
        self,
        query_embedding: list[float],
        top_k: int
    ) -> list[RetrievedChunk]:

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],

            n_results=top_k,

            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]

        retrieved_chunks = []

        for index, (
            document,
            metadata,
            distance,
            point_id,
        ) in enumerate(
            zip(
                documents,
                metadatas,
                distances,
                ids,
            ),
            start=1
        ):

            # Chroma returns cosine distance.
            #
            # cosine similarity = 1 - cosine distance
            #
            score = 1.0 - distance

            retrieved_chunks.append(
                RetrievedChunk(
                    document_id=UUID(
                        metadata["document_id"]
                    ),

                    filename=metadata[
                        "filename"
                    ],

                    chunk_index=metadata[
                        "chunk_index"
                    ],

                    text=document,

                    score=score,

                    rank=index,

                    vector_store="chroma",

                    collection_name=(
                        COLLECTION_NAME
                    ),

                    point_id=point_id,
                )
            )

        return retrieved_chunks

    # =========================================================
    # COUNT
    # =========================================================

    def count(self) -> int:

        return self.collection.count()

    # =========================================================
    # INFO
    # =========================================================

    def info(self) -> dict:

        return {
            "vector_store": "chroma",

            "collection_name": (
                COLLECTION_NAME
            ),

            "count": self.collection.count(),

            "vector_size": None,

            "distance": "cosine",

            "storage": CHROMA_DB_PATH,
        }

    # =========================================================
    # INSPECT
    # =========================================================

    def inspect(
        self,
        limit: int = 10
    ) -> list[dict]:

        result = self.collection.get(
            limit=limit,

            include=[
                "documents",
                "metadatas",
            ],
        )

        ids = result["ids"]
        documents = result["documents"]
        metadatas = result["metadatas"]

        records = []

        for index, (
            point_id,
            document,
            metadata,
        ) in enumerate(
            zip(
                ids,
                documents,
                metadatas,
            )
        ):

            records.append(
                {
                    "record_index": index,

                    "point_id": point_id,

                    "document_id": metadata.get(
                        "document_id"
                    ),

                    "filename": metadata.get(
                        "filename"
                    ),

                    "chunk_index": metadata.get(
                        "chunk_index"
                    ),

                    "text": document,
                }
            )

        return records