from langchain_chroma import Chroma

from langchain_core.documents import Document

from legal_ai_app.core.config import settings
from legal_ai_app.services.embedding_service import EmbeddingService


class VectorStore:

    def __init__(self):

        embedding_service = EmbeddingService()

        self.vector_db = Chroma(
            collection_name="legal_documents",
            persist_directory=settings.CHROMA_DIR,
            embedding_function=embedding_service.get_embeddings(),
        )

    def add_documents(self, chunks):

        documents = []

        for index, chunk in enumerate(chunks):

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "chunk_id": index
                    }
                )
            )

        self.vector_db.add_documents(documents)


    def similarity_search(self, query: str, k: int = 5):

        return self.vector_db.similarity_search(
        query=query,
        k=k
        )
    def count(self):
        return self.vector_db._collection.count()