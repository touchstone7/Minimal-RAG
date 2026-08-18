from src.config import TOP_K

from src.embeddings.embeddings_service import (
    embed_query
)

from src.models import RetrievedChunk

from src.vectordb.vector_store import VectorStore


def retrieve(
    vector_store: VectorStore,
    question: str,
    top_k: int = TOP_K,
) -> list[RetrievedChunk]:

    query_embedding = embed_query(
        question
    )

    return vector_store.search(
        query_embedding=query_embedding,
        top_k=top_k,
    )