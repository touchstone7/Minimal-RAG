from dataclasses import dataclass
from pathlib import Path
from models import Document

def load_documents(directory: str) -> list[Document]:
    """
    Load all .txt documents from the given directory.

    Args:
        directory: Path to the directory containing text files.

    Returns:
        List of Document objects.
    """

    documents: list[Document] = []

    data_path = Path(directory)

    if not data_path.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for file in data_path.glob("*.txt"):

        content = file.read_text(encoding="utf-8")

        documents.append(
            Document(
                filename=file.name,
                content=content
            )
        )

    return documents