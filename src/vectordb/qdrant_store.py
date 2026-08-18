from uuid import UUID, uuid5

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from src.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION_NAME,
    QDRANT_VECTOR_SIZE,
)

from src.models import (
    EmbeddedChunk,
    RetrievedChunk,
)

from src.vectordb.vector_store import VectorStore


class QdrantVectorStore(VectorStore):

    # =========================================================
    # CONSTRUCTOR
    # =========================================================

    def __init__(self):

        self.client = None

        self.collection_name = (
            QDRANT_COLLECTION_NAME
        )

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def initialize(self) -> None:

        if not QDRANT_URL:

            raise ValueError(
                "QDRANT_URL is not configured."
            )

        if not QDRANT_API_KEY:

            raise ValueError(
                "QDRANT_API_KEY is not configured."
            )

        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )

        collections = (
            self.client.get_collections()
        )

        existing_names = {
            collection.name
            for collection in (
                collections.collections
            )
        }

        if self.collection_name not in existing_names:

            self.client.create_collection(
                collection_name=(
                    self.collection_name
                ),

                vectors_config=VectorParams(
                    size=QDRANT_VECTOR_SIZE,

                    distance=Distance.COSINE,
                ),
            )

    # =========================================================
    # POINT ID
    # =========================================================

    @staticmethod
    def _generate_chunk_id(
        chunk: EmbeddedChunk
    ) -> str:

        return str(
            uuid5(
                chunk.document_id,
                str(chunk.chunk_index)
            )
        )

    # =========================================================
    # INDEX
    # =========================================================

    def index(
        self,
        chunks: list[EmbeddedChunk]
    ) -> None:

        if not chunks:
            return

        points = []

        for chunk in chunks:

            point_id = (
                self._generate_chunk_id(
                    chunk
                )
            )

            points.append(
                PointStruct(
                    id=point_id,

                    vector=chunk.embedding,

                    payload={
                        "document_id": str(
                            chunk.document_id
                        ),

                        "filename": (
                            chunk.filename
                        ),

                        "chunk_index": (
                            chunk.chunk_index
                        ),

                        "text": chunk.text,
                    },
                )
            )

        self.client.upsert(
            collection_name=(
                self.collection_name
            ),

            points=points,

            wait=True,
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def search(
        self,
        query_embedding: list[float],
        top_k: int
    ) -> list[RetrievedChunk]:

        results = self.client.query_points(
            collection_name=(
                self.collection_name
            ),

            query=query_embedding,

            limit=top_k,

            with_payload=True,

            with_vectors=False,
        )

        retrieved_chunks = []

        for rank, point in enumerate(
            results.points,
            start=1
        ):

            payload = (
                point.payload or {}
            )

            retrieved_chunks.append(
                RetrievedChunk(
                    document_id=UUID(
                        payload["document_id"]
                    ),

                    filename=payload[
                        "filename"
                    ],

                    chunk_index=payload[
                        "chunk_index"
                    ],

                    text=payload[
                        "text"
                    ],

                    score=float(
                        point.score
                    ),

                    rank=rank,

                    vector_store="qdrant",

                    collection_name=(
                        self.collection_name
                    ),

                    point_id=str(
                        point.id
                    ),
                )
            )

        return retrieved_chunks

    # =========================================================
    # COUNT
    # =========================================================

    def count(self) -> int:

        info = self.client.get_collection(
            collection_name=(
                self.collection_name
            )
        )

        return info.points_count

    # =========================================================
    # INFO
    # =========================================================

    def info(self) -> dict:

        info = self.client.get_collection(
            collection_name=(
                self.collection_name
            )
        )

        return {
            "vector_store": "qdrant",

            "collection_name": (
                self.collection_name
            ),

            "count": info.points_count,

            "vector_size": (
                QDRANT_VECTOR_SIZE
            ),

            "distance": "cosine",
        }

    # =========================================================
    # INSPECT
    # =========================================================

    def inspect(
        self,
        limit: int = 10
    ) -> list[dict]:

        records, _ = self.client.scroll(
            collection_name=(
                self.collection_name
            ),

            limit=limit,

            with_payload=True,

            with_vectors=False,
        )

        inspected_records = []

        for index, record in enumerate(
            records
        ):

            payload = (
                record.payload or {}
            )

            inspected_records.append(
                {
                    "record_index": index,

                    "point_id": str(
                        record.id
                    ),

                    "document_id": payload.get(
                        "document_id"
                    ),

                    "filename": payload.get(
                        "filename"
                    ),

                    "chunk_index": payload.get(
                        "chunk_index"
                    ),

                    "text": payload.get(
                        "text",
                        ""
                    ),
                }
            )

        return inspected_records