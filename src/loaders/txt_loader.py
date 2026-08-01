from pathlib import Path

from src.models import Document


def load_txt_documents(directory: str) -> list[Document]:
    """
    Load every .txt file inside a directory.
    """

    documents: list[Document] = []

    data_path = Path(directory)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Directory '{directory}' does not exist."
        )

    for file in data_path.glob("*.txt"):

        documents.append(
            Document(
                filename=file.name,
                content=file.read_text(
                    encoding="utf-8"
                )
            )
        )

    return documents