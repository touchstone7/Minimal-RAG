import ollama


def ask_llm(
    prompt: str,
    model: str = "qwen3:8b"
) -> str:
    """
    Send the prompt to the LLM and return its response.
    """

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]