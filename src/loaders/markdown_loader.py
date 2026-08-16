from pathlib import Path
from uuid import UUID

from src.models import Document


def load_markdown_document(
    file_path: Path,
    document_id: UUID
) -> Document:

    return Document(
        document_id=document_id,
        filename=file_path.name,
        content=file_path.read_text(
            encoding="utf-8"
        )
    )