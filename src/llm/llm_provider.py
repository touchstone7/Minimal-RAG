from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract interface for all LLM providers.

    RagService depends on this interface rather than
    directly depending on a specific LLM implementation.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the supplied prompt.
        """

        pass