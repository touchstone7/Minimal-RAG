from src.config import LLM_PROVIDER

from src.llm.llm_provider import LLMProvider
from src.llm.ollama_provider import OllamaProvider
from src.llm.gemini_provider import GeminiProvider


def get_llm_provider() -> LLMProvider:
    """
    Create the configured LLM provider.

    Supported providers:
        - ollama
        - gemini
    """

    provider = LLM_PROVIDER.lower()

    if provider == "ollama":

        return OllamaProvider()

    if provider == "gemini":

        return GeminiProvider()

    raise ValueError(
        f"Unknown LLM provider: {LLM_PROVIDER}. "
        f"Supported providers: ollama, gemini"
    )