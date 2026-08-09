from fastapi import APIRouter, UploadFile, File

from legal_ai_app.models.schemas import (
    UploadResponse,
    ChatRequest,
    AskResponse,
    SessionResponse,
)

from legal_ai_app.services.upload_service import UploadService
from legal_ai_app.services.vector_store import VectorStore
from legal_ai_app.services.citation_service import CitationService
from legal_ai_app.services.query_classifier import QueryClassifier
from legal_ai_app.services.legal_response_service import LegalResponseService
from legal_ai_app.services.conversation_service import ConversationService

from legal_ai_app.rag.hybrid_retriever import HybridRetriever
from legal_ai_app.rag.context_builder import ContextBuilder


router = APIRouter()

upload_service = UploadService()
vector_store = VectorStore()
citation_service = CitationService()
query_classifier = QueryClassifier()
hybrid_retriever = HybridRetriever()
context_builder = ContextBuilder()
legal_response_service = LegalResponseService()
conversation_service = ConversationService()


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_pdf(
    file: UploadFile = File(...)
):

    result = upload_service.process_pdf(file)

    return {
        "message": "File uploaded successfully.",
        "filename": result["filename"],
        "characters": result["characters"],
        "chunks": len(result["chunks"]),
    }


@router.post(
    "/session",
    response_model=SessionResponse
)
async def create_session():

    session_id = conversation_service.create_session()

    return SessionResponse(
        session_id=session_id
    )


@router.post(
    "/ask",
    response_model=AskResponse
)
async def ask_question(
    request: ChatRequest
):

    # Get previous conversation.
    history = conversation_service.get_history(
        request.session_id
    )

    # Classify the current question.
    classification = query_classifier.classify(
        request.question
    )

    print("\n" + "=" * 80)
    print("QUERY CLASSIFICATION")
    print(classification)

    # Retrieve relevant documents.
    documents = hybrid_retriever.retrieve(
        question=request.question,
        category=classification.category,
        user_k=5,
        legal_k=5,
        top_k=5,
    )

    print("=" * 80)
    print("Retrieved:", len(documents), "documents")

    for i, doc in enumerate(documents):

        print(f"\nChunk {i + 1}")

        print("Source:")
        print(
            doc.metadata.get(
                "retrieval_source"
            )
        )

        print("Metadata:")
        print(doc.metadata)

        print("Text:")
        print(
            doc.page_content[:300]
        )

    # Build clean context for the LLM.
    context = context_builder.build(
        documents
    )

    # Generate legal response.
    answer = legal_response_service.generate(
        question=request.question,
        classification=classification,
        context=context,
        history=history,
    )

    # Save conversation.
    conversation_service.add_message(
        session_id=request.session_id,
        role="user",
        content=request.question,
    )

    conversation_service.add_message(
        session_id=request.session_id,
        role="assistant",
        content=answer,
    )

    # Build citations.
    sources = citation_service.build_sources(
        documents
    )

    return AskResponse(
        answer=answer,
        sources=sources,
    )