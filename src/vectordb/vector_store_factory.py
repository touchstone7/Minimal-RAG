from src.config import VECTOR_DB

from src.vectordb.vector_store import (
    VectorStore,
)

from src.vectordb.chroma_store import (
    ChromaVectorStore,
)

from src.vectordb.qdrant_store import (
    QdrantVectorStore,
)


def get_vector_store() -> VectorStore:

    provider = VECTOR_DB.lower()

    if provider == "chroma":

        store = ChromaVectorStore()

    elif provider == "qdrant":

        store = QdrantVectorStore()

    else:

        raise ValueError(
            f"Unsupported VECTOR_DB: "
            f"{VECTOR_DB}. "
            f"Supported values: "
            f"'chroma', 'qdrant'."
        )

    store.initialize()

    return store