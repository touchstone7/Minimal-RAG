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

from src.models import EmbeddedChunk


# =========================================================
# QDRANT CLIENT
# =========================================================

def create_client() -> QdrantClient:

    if not QDRANT_URL:
        raise ValueError(
            "QDRANT_URL is not configured."
        )

    if not QDRANT_API_KEY:
        raise ValueError(
            "QDRANT_API_KEY is not configured."
        )

    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )


# =========================================================
# COLLECTION
# =========================================================

def create_collection(
    client: QdrantClient
):

    collections = client.get_collections()

    existing_names = {
        collection.name
        for collection in collections.collections
    }

    if QDRANT_COLLECTION_NAME not in existing_names:

        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=QDRANT_VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        print(
            f"Created Qdrant collection: "
            f"{QDRANT_COLLECTION_NAME}"
        )

    else:

        print(
            f"Using existing Qdrant collection: "
            f"{QDRANT_COLLECTION_NAME}"
        )

    return client


# =========================================================
# POINT ID
# =========================================================

def _generate_chunk_id(
    chunk: EmbeddedChunk
) -> str:

    """
    Generate a deterministic UUID from:

        document_id + chunk_index

    This means:

        same document + same chunk index
            -> same Qdrant point ID

        different document
            -> different Qdrant point ID
    """

    return str(
        uuid5(
            chunk.document_id,
            str(chunk.chunk_index)
        )
    )


# =========================================================
# INDEX CHUNKS
# =========================================================

def index_chunks(
    client: QdrantClient,
    chunks: list[EmbeddedChunk]
):

    points = []

    for chunk in chunks:

        point_id = _generate_chunk_id(
            chunk
        )

        points.append(
            PointStruct(
                id=point_id,

                vector=chunk.embedding,

                payload={
                    "document_id": str(
                        chunk.document_id
                    ),

                    "filename": chunk.filename,

                    "chunk_index": chunk.chunk_index,

                    "text": chunk.text,
                }
            )
        )

    if not points:
        return

    client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        points=points,
        wait=True,
    )


# =========================================================
# COLLECTION INFO
# =========================================================

def show_collection_info(
    client: QdrantClient
):

    info = client.get_collection(
        collection_name=QDRANT_COLLECTION_NAME
    )

    print(
        "\n========== QDRANT COLLECTION =========="
    )

    print(
        f"Collection: "
        f"{QDRANT_COLLECTION_NAME}"
    )

    print(
        f"Points: "
        f"{info.points_count}"
    )

    print(
        f"Vector size: "
        f"{QDRANT_VECTOR_SIZE}"
    )

    print(
        "Distance: COSINE"
    )

    print(
        "=======================================\n"
    )


# =========================================================
# INSPECT COLLECTION
# =========================================================

def inspect_collection(
    client: QdrantClient,
    limit: int = 10
):

    print(
        "\n========== QDRANT RECORDS =========="
    )

    records, _ = client.scroll(
        collection_name=QDRANT_COLLECTION_NAME,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )

    for index, record in enumerate(records):

        print(
            f"\nRecord #{index}"
        )

        print(
            f"Qdrant ID: "
            f"{record.id}"
        )

        payload = record.payload or {}

        print(
            f"Document ID: "
            f"{payload.get('document_id')}"
        )

        print(
            f"Filename: "
            f"{payload.get('filename')}"
        )

        print(
            f"Chunk Index: "
            f"{payload.get('chunk_index')}"
        )

        text = payload.get(
            "text",
            ""
        )

        print(
            f"Text: "
            f"{text[:200]}"
        )

    print(
        "\n====================================\n"
    )

# =========================================================
# SEARCH
# =========================================================

def search(
    client: QdrantClient,
    query_embedding: list[float],
    top_k: int = 3,
):
    results = client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        with_payload=True,
        with_vectors=False,
    )

    return results.points