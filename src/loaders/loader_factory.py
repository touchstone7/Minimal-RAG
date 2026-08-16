from pathlib import Path
from uuid import UUID

from src.models import Document

from src.loaders.txt_loader import load_txt_document
from src.loaders.markdown_loader import load_markdown_document
from src.loaders.pdf_loader import load_pdf_document
from src.loaders.docx_loader import load_docx_document


def load_document(
    file_path: Path,
    document_id: UUID
) -> Document:

    extension = file_path.suffix.lower()

    if extension == ".txt":

        return load_txt_document(
            file_path,
            document_id
        )

    if extension == ".md":

        return load_markdown_document(
            file_path,
            document_id
        )

    if extension == ".pdf":

        return load_pdf_document(
            file_path,
            document_id
        )

    if extension == ".docx":

        return load_docx_document(
            file_path,
            document_id
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )