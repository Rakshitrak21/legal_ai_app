import os

from legal_ai_app.services.pdf_loader import PDFLoader
from legal_ai_app.services.text_splitter import TextSplitter
from legal_ai_app.services.vector_store import VectorStore


class KnowledgeBase:

    def __init__(self):

        self.pdf_loader = PDFLoader()
        self.text_splitter = TextSplitter()
        self.vector_store = VectorStore()

    def ingest_document(
        self,
        file_path: str,
        document_type: str,
        source: str,
        category: str,
        court: str | None = None,
        case_name: str | None = None,
        year: int | None = None,
        citation: str | None = None,
    ):

        pages = self.pdf_loader.load_pages(file_path)

        total_chunks = 0

        for page_data in pages:

            page_number = page_data["page"]
            page_text = page_data["text"]

            chunks = self.text_splitter.split_text(page_text)

            metadata = {
                "source": source,
                "document_type": document_type,
                "category": category,
                "page": page_number,
            }

            if court:
                metadata["court"] = court

            if case_name:
                metadata["case_name"] = case_name

            if year:
                metadata["year"] = year

            if citation:
                metadata["citation"] = citation

            self.vector_store.add_documents(
                chunks=chunks,
                collection_name="legal_knowledge",
                metadata=metadata,
            )

            total_chunks += len(chunks)

        return {
            "file": os.path.basename(file_path),
            "characters": sum(
                len(page["text"])
                for page in pages
            ),
            "chunks": total_chunks,
            "pages": len(pages),
        }