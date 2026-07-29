from pathlib import Path

from docx import Document as DocxDocument

from models import Document


def load_docx_documents(
    directory: str
) -> list[Document]:

    documents: list[Document] = []

    data_path = Path(directory)

    for file in data_path.glob("*.docx"):

        doc = DocxDocument(file)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

        documents.append(
            Document(
                filename=file.name,
                content=text
            )
        )

    return documents