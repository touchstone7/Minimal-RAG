def build_prompt(question: str, retrieved_chunks) -> str:
    """
    Build the final prompt sent to the language model.
    """

    context = ""

    documents = retrieved_chunks["documents"][0]

    for index, chunk in enumerate(documents, start=1):

        context += f"Context {index}:\n"
        context += chunk
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