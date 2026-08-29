from src.config import LLM_PROVIDER, VECTOR_STORE
from src.services.rag_service import RagService


# =========================================================
# SAMPLE QUESTION
# =========================================================

SAMPLE_QUESTION = (
    "What is the main concept discussed in the "
    "provided documents?"
)


# =========================================================
# DISPLAY
# =========================================================

def print_header():
    print("\n" + "=" * 50)
    print("           MINIMAL-RAG BACKEND CLI")
    print("=" * 50)

    print(
        f"Vector store : {VECTOR_STORE}"
    )

    print(
        f"LLM provider : {LLM_PROVIDER}"
    )

    print("=" * 50)


# =========================================================
# SAMPLE TEST
# =========================================================

def run_sample_test(rag: RagService):

    print("\nRunning backend smoke test...")

    print(
        f"\nQuestion:\n{SAMPLE_QUESTION}"
    )

    print("\nRetrieving context...")
    
    answer = rag.query(
        SAMPLE_QUESTION
    )

    print("\nAnswer")
    print("=" * 50)
    print(answer)
    print("=" * 50)

    print(
        "\nBackend smoke test completed successfully."
    )


# =========================================================
# CUSTOM QUERY
# =========================================================

def run_custom_query(rag: RagService):

    question = input(
        "\nAsk a question: "
    ).strip()

    if not question:

        print(
            "\nQuestion cannot be empty."
        )

        return

    print(
        "\nRetrieving context..."
    )

    answer = rag.query(
        question
    )

    print("\nAnswer")
    print("=" * 50)
    print(answer)
    print("=" * 50)


# =========================================================
# MAIN
# =========================================================

def main():

    print_header()

    try:

        rag = RagService()

        if rag.vector_store.count() == 0:

            print(
                "\nKnowledge base is empty."
            )

            print(
                "Use the FastAPI /ingest endpoint "
                "to ingest a document first."
            )

            return

        print(
            "\n1. Run sample backend test"
        )

        print(
            "2. Ask a custom question"
        )

        print(
            "3. Exit"
        )

        choice = input(
            "\nSelect an option: "
        ).strip()

        if choice == "1":

            run_sample_test(
                rag
            )

        elif choice == "2":

            run_custom_query(
                rag
            )

        elif choice == "3":

            print(
                "\nExiting."
            )

        else:

            print(
                "\nInvalid option."
            )

    except Exception as error:

        print(
            "\nBackend test failed."
        )

        print(
            f"Error: {error}"
        )


if __name__ == "__main__":
    main()