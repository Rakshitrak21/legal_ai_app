from legal_ai_app.services.vector_store import VectorStore


class LegalRAG:

    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(
        self,
        question: str,
        category: str | None = None,
        k: int = 5,
    ):

        metadata_filter = None

        if category:
            metadata_filter = {
                "category": category
            }

        return self.vector_store.similarity_search(
            query=question,
            collection_name="legal_knowledge",
            k=k,
            filter=metadata_filter,
        )