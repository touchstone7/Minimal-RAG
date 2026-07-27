from documents import load_documents


def main():

    documents = load_documents("data")

    print(f"Loaded {len(documents)} document(s)\n")

    for document in documents:

        print(document.filename)

        print("-" * 40)

        print(document.content)

        print()


if __name__ == "__main__":
    main()