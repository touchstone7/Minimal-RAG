from google import genai

from src.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

from src.llm.llm_provider import LLMProvider


class GeminiProvider(LLMProvider):
    """
    LLM provider implementation for Google's Gemini API.
    """

    def __init__(
        self,
        api_key: str = GEMINI_API_KEY,
        model: str = GEMINI_MODEL,
    ):

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.model = model

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text