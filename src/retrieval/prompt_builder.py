from src.models import RetrievedChunk


def build_prompt(
    question: str,
    retrieved_chunks: list[RetrievedChunk]
) -> str:
    """
    Build the final prompt sent to the language model.
    """

    context = ""

    for index, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        context += (
            f"Context {index}:\n"
        )

        context += chunk.text

        context += "\n\n"

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, simply say:

"I don't know based on the provided documents."

====================

{context}

====================

Question:
{question}

Answer:
"""

    return prompt