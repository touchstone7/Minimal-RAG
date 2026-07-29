from models import Document

from loaders.txt_loader import load_txt_documents
from loaders.markdown_loader import (
    load_markdown_documents
)

from loaders.pdf_loader import (
    load_pdf_documents
)

from loaders.docx_loader import (
    load_docx_documents
)

def load_documents(
    directory: str
) -> list[Document]:

    documents: list[Document] = []

    documents.extend(
        load_txt_documents(directory)
    )

    documents.extend(
        load_markdown_documents(directory)
    )

    documents.extend(
        load_pdf_documents(directory)
    )
    documents.extend(
        load_docx_documents(directory)
    )

    return documents