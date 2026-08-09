from legal_ai_app.rag.user_document_rag import UserDocumentRAG
from legal_ai_app.rag.legal_rag import LegalRAG
from legal_ai_app.rag.reranker import Reranker


class HybridRetriever:

    def __init__(self):

        self.user_rag = UserDocumentRAG()
        self.legal_rag = LegalRAG()
        self.reranker = Reranker()

    def retrieve(
        self,
        question: str,
        category: str | None = None,
        user_k: int = 5,
        legal_k: int = 5,
        top_k: int = 5,
    ):

        # Retrieve user documents.
        user_documents = self.user_rag.retrieve(
            question,
            user_k,
        )

        # Retrieve relevant legal knowledge.
        legal_documents = self.legal_rag.retrieve(
            question,
            category=category,
            k=legal_k,
        )

        # Mark retrieval source.
        for document in user_documents:

            document.metadata[
                "retrieval_source"
            ] = "user_document"

        for document in legal_documents:

            document.metadata[
                "retrieval_source"
            ] = "legal_knowledge"

        # Combine both retrievers.
        documents = user_documents + legal_documents

        # Remove duplicate chunks from the same source.
        unique_documents = []
        seen = set()

        for document in documents:

            content = document.page_content.strip()

            source = document.metadata.get(
                "retrieval_source"
            )

            key = (source, content)

            if key not in seen:

                seen.add(key)
                unique_documents.append(document)

        # Rerank all candidates.
        reranked_documents = self.reranker.rerank(
            question=question,
            documents=unique_documents,
            top_k=top_k,
        )

        return reranked_documents