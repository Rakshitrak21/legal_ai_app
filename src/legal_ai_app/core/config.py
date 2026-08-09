from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    UPLOAD_DIR = "src/legal_ai_app/storage/uploads"

    CHROMA_DIR = "src/legal_ai_app/storage/chroma"

    KNOWLEDGE_BASE_DIR = "src/legal_ai_app/storage/knowledge_base"

    CHUNK_SIZE = 1000

    CHUNK_OVERLAP = 200

    EMBEDDING_MODEL = "text-embedding-3-small"

    CHAT_MODEL = "gpt-4o-mini"


settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DIR, exist_ok=True)
os.makedirs(settings.KNOWLEDGE_BASE_DIR,exist_ok=True)
