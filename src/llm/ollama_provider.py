import ollama

from src.config import CHAT_MODEL

from src.llm.llm_provider import LLMProvider


class OllamaProvider(LLMProvider):
    """
    LLM provider implementation for local Ollama inference.
    """

    def __init__(
        self,
        model: str = CHAT_MODEL
    ):
        self.model = model

    def generate(
        self,
        prompt: str
    ) -> str:

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]