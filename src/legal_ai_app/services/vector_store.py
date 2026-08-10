from langchain_chroma import Chroma
from langchain_core.documents import Document

from legal_ai_app.core.config import settings
from legal_ai_app.services.embedding_service import EmbeddingService


class VectorStore:

    def __init__(self):
        self.embeddings = EmbeddingService().get_embeddings()

    def get_collection(self, collection_name: str):

        return Chroma(
            collection_name=collection_name,
            persist_directory=settings.CHROMA_DIR,
            embedding_function=self.embeddings,
        )

    def add_documents(
        self,
        chunks: list[str],
        collection_name: str,
        metadata: dict | None = None,
    ):

        db = self.get_collection(collection_name)

        documents = []

        for index, chunk in enumerate(chunks):

            chunk_metadata = {
                "chunk_id": index,
                **(metadata or {}),
            }

            documents.append(
                Document(
                    page_content=chunk,
                    metadata=chunk_metadata,
                )
            )

        db.add_documents(documents)

    def similarity_search(
        self,
        query: str,
        collection_name: str = "user_documents",
        category: str | None = None,
        document_type: str | None = None,
        k: int = 5,
    ):

        db = self.get_collection(
            collection_name
        )

        filters = []

        if category:
            filters.append({
                "category": category
            })

        if document_type:
            filters.append({
                "document_type": document_type
            })

        filter_condition = None

        if len(filters) == 1:

            filter_condition = filters[0]

        elif len(filters) > 1:

            filter_condition = {
                "$and": filters
            }

        return db.similarity_search(
            query=query,
            k=k,
            filter=filter_condition,
        )

    def count(self, collection_name: str):

        db = self.get_collection(
            collection_name
        )

        return db._collection.count()