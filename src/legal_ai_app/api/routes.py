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
from legal_ai_app.services.legal_issue_analyzer import LegalIssueAnalyzer
from legal_ai_app.rag.hybrid_retriever import HybridRetriever
from legal_ai_app.rag.context_builder import ContextBuilder
from legal_ai_app.services.legal_provision_finder import LegalProvisionFinder
from legal_ai_app.services.research_planner import ResearchPlanner




router = APIRouter()

upload_service = UploadService()
vector_store = VectorStore()
citation_service = CitationService()
query_classifier = QueryClassifier()
legal_issue_analyzer = LegalIssueAnalyzer()
hybrid_retriever = HybridRetriever()
context_builder = ContextBuilder()
legal_response_service = LegalResponseService()
conversation_service = ConversationService()
legal_provision_finder = LegalProvisionFinder()
research_planner = ResearchPlanner()


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

    issue_analysis = legal_issue_analyzer.analyze(
        request.question
    )

    research_plan = research_planner.create_plan(
        question=request.question,
        classification=classification,
        issue_analysis=issue_analysis,
    )

    legal_provisions = legal_provision_finder.find(
        question=request.question,
        issue_analysis=issue_analysis,
    )

    print("\n" + "=" * 80)
    print("QUERY CLASSIFICATION")
    print(classification)

    print("\nLEGAL ISSUE ANALYSIS")
    print(issue_analysis)

    print("\nRESEARCH PLAN")
    print(research_plan)

    print("\nLEGAL PROVISIONS")
    print(legal_provisions)

    # Retrieve relevant documents.
    documents = hybrid_retriever.retrieve(
        question=request.question,
        category=classification.category,
        retrieval_queries=issue_analysis.get(
            "retrieval_queries",
            [],
        ),
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
        legal_provisions=legal_provisions,
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