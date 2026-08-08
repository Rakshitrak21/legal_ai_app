from langchain_openai import OpenAIEmbeddings

from legal_ai_app.core.config import settings


class EmbeddingService:

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )

    def get_embeddings(self):
        return self.embeddings