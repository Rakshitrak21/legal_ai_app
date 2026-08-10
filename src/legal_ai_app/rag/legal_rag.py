from legal_ai_app.services.vector_store import VectorStore


class LegalRAG:

    def __init__(self):

        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        category: str | None = None,
        document_type: str | None = None,
        k: int = 5,
    ):

        return self.vector_store.similarity_search(
            query=query,
            collection_name="legal_knowledge",
            category=category,
            document_type=document_type,
            k=k,
        )