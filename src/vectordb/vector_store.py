from abc import ABC, abstractmethod

from src.models import EmbeddedChunk, RetrievedChunk


class VectorStore(ABC):

    # =========================================================
    # INITIALIZATION
    # =========================================================

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the vector store and make it ready for use.
        """
        pass

    # =========================================================
    # INDEXING
    # =========================================================

    @abstractmethod
    def index(
        self,
        chunks: list[EmbeddedChunk]
    ) -> None:
        """
        Store embedded chunks in the vector database.
        """
        pass

    # =========================================================
    # SEARCH
    # =========================================================

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int
    ) -> list[RetrievedChunk]:
        """
        Search for the chunks most relevant to the query
        embedding.

        The database-specific result is converted into
        RetrievedChunk objects before being returned.
        """
        pass

    # =========================================================
    # COUNT
    # =========================================================

    @abstractmethod
    def count(self) -> int:
        """
        Return the number of stored chunks.
        """
        pass

    # =========================================================
    # INFO
    # =========================================================

    @abstractmethod
    def info(self) -> dict:
        """
        Return structured information about the vector store
        and its collection.
        """
        pass

    # =========================================================
    # INSPECTION
    # =========================================================

    @abstractmethod
    def inspect(
        self,
        limit: int = 10
    ) -> list[dict]:
        """
        Return structured information about stored records.

        This method must not print directly.
        """
        pass