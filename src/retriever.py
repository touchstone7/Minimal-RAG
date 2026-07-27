import ollama


def retrieve(
    collection,
    question: str,
    model: str = "nomic-embed-text",
    top_k: int = 3
):
    response = ollama.embed(
        model=model,
        input=question
    )

    question_embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    return results