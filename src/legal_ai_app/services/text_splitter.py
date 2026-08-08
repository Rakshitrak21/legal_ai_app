from langchain_text_splitters import RecursiveCharacterTextSplitter

from legal_ai_app.core.config import settings


class TextSplitter:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split_text(self, text: str):
        return self.splitter.split_text(text)