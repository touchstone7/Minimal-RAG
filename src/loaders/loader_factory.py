from src.models import Document

from src.loaders.txt_loader import load_txt_documents
from src.loaders.markdown_loader import load_markdown_documents
from src.loaders.pdf_loader import load_pdf_documents
from src.loaders.docx_loader import load_docx_documents


def load_documents(
    directory: str
) -> list[Document]:

    documents: list[Document] = []

    loaders = [
        load_txt_documents,
        load_markdown_documents,
        load_pdf_documents,
        load_docx_documents,
    ]

    for loader in loaders:
        documents.extend(
            loader(directory)
        )

    return documents