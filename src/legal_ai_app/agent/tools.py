from legal_ai_app.rag.legal_rag import LegalRAG
from legal_ai_app.rag.user_document_rag import UserDocumentRAG
from legal_ai_app.services.document_analysis_service import (
    DocumentAnalysisService,
)


legal_rag = LegalRAG()
user_rag = UserDocumentRAG()
document_analysis_service = DocumentAnalysisService()


def search_legal_knowledge(
    query: str,
    k: int = 5,
):

    return legal_rag.retrieve(
        query=query,
        k=k,
    )


def search_judgments(
    query: str,
    k: int = 5,
):

    return legal_rag.retrieve(
        query=query,
        document_type="judgment",
        k=k,
    )


def search_user_documents(
    query: str,
    k: int = 5,
):

    return user_rag.retrieve(
        question=query,
        k=k,
    )


def analyze_user_document(
    question: str,
    k: int = 8,
):

    documents = user_rag.retrieve(
        question=question,
        k=k,
    )

    return document_analysis_service.analyze(
        question=question,
        documents=documents,
    )