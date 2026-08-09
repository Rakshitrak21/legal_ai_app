import os
import shutil

from legal_ai_app.core.config import settings
from legal_ai_app.services.pdf_loader import PDFLoader
from legal_ai_app.services.text_splitter import TextSplitter
from legal_ai_app.services.vector_store import VectorStore


class UploadService:

    def __init__(self):
        self.pdf_loader = PDFLoader()
        self.text_splitter = TextSplitter()
        self.vector_store = VectorStore()

    def process_pdf(self, file):

        file_path = os.path.join(
            settings.UPLOAD_DIR,
            file.filename,
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        pdf_text = self.pdf_loader.load_pdf(file_path)

        chunks = self.text_splitter.split_text(pdf_text)

        self.vector_store.add_documents(
            chunks=chunks,
            collection_name="user_documents",
            metadata={
                "source": file.filename,
                "document_type": "user_upload",
            },
        )

        print(
            "Stored",
            len(chunks),
            "chunks in user_documents"
        )

        return {
            "filename": file.filename,
            "characters": len(pdf_text),
            "chunks": chunks,
        }