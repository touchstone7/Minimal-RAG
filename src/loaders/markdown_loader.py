from pathlib import Path

from src.models import Document


def load_markdown_documents(
    directory: str
) -> list[Document]:

    documents: list[Document] = []

    data_path = Path(directory)

    for file in data_path.glob("*.md"):

        documents.append(
            Document(
                filename=file.name,
                content=file.read_text(
                    encoding="utf-8"
                )
            )
        )

    return documents