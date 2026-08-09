from legal_ai_app.services.vector_store import VectorStore


class UserDocumentRAG:

    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, question: str, k: int = 5):

        return self.vector_store.similarity_search(
            query=question,
            collection_name="user_documents",
            k=k,
        )