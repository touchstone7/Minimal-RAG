from services.rag_service import RagService


def main():

    rag = RagService()

    rag.ingest()

    question = input(
        "\nAsk a question: "
    )

    answer = rag.query(question)

    print("\nAnswer")
    print("=" * 60)
    print(answer)
    print("=" * 60)


if __name__ == "__main__":
    main()