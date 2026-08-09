from fastapi import APIRouter, UploadFile, File, Form

from legal_ai_app.rag.knowledge_base import KnowledgeBase
from legal_ai_app.core.config import settings
from legal_ai_app.core.constants import DocumentType, LegalCategory


router = APIRouter(
    prefix="/knowledge",
    tags=["Legal Knowledge Base"],
)

knowledge_base = KnowledgeBase()


@router.post("/ingest")
async def ingest_legal_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(...),
    category: LegalCategory = Form(...),
    court: str | None = Form(None),
    case_name: str | None = Form(None),
    year: int | None = Form(None),
    citation: str | None = Form(None),
):

    file_path = f"{settings.KNOWLEDGE_BASE_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = knowledge_base.ingest_document(
        file_path=file_path,
        document_type=document_type,
        source=file.filename,
        category=category,
        court=court,
        case_name=case_name,
        year=year,
        citation=citation,
    )

    return {
        "message": "Legal document added to knowledge base.",
        **result,
    }