from fastapi import APIRouter, UploadFile, File
from legal_ai_app.models.schemas import (UploadResponse,AskRequest,AskResponse)
from legal_ai_app.core.config import settings
from legal_ai_app.services.pdf_loader import PDFLoader
from legal_ai_app.services.text_splitter import TextSplitter
from legal_ai_app.services.vector_store import VectorStore
from legal_ai_app.services.upload_service import UploadService
from legal_ai_app.services.llm_service import LLMService

import shutil
import os

router = APIRouter()
pdf_loader = PDFLoader()
text_splitter = TextSplitter()
vector_store = VectorStore()
upload_service=UploadService()
llm_service = LLMService()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):

    result = upload_service.process_pdf(file)

    return {
        "message": "File uploaded successfully.",
        "filename": result["filename"],
        "characters": result["characters"],
        "chunks": len(result["chunks"])
    }

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):

    documents = vector_store.similarity_search(request.question)

    print("=" * 80)
    print("Retrieved:", len(documents), "documents")

    for i, doc in enumerate(documents):
        print(f"\nChunk {i + 1}")
        print(doc.page_content[:500])
    
        context = "\n\n".join(
            doc.page_content
            for doc in documents
        )

    answer = llm_service.ask(
        context=context,
        question=request.question
    )

    return AskResponse(
        answer=answer
    )

    


