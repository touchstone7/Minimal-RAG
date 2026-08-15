from pathlib import Path
from uuid import uuid4

from pypdf import PdfReader

from src.models import Document


def load_pdf_documents(
    directory: str
) -> list[Document]:

    documents: list[Document] = []

    data_path = Path(directory)

    for file in data_path.glob("*.pdf"):

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        documents.append(
            Document(
                document_id=uuid4(),
                filename=file.name,
                content=text
            )
        )

    return documents