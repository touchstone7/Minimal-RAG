from pathlib import Path
from uuid import UUID

from pypdf import PdfReader

from src.models import Document


def load_pdf_document(
    file_path: Path,
    document_id: UUID
) -> Document:

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return Document(
        document_id=document_id,
        filename=file_path.name,
        content=text
    )