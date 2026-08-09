from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    filename: str
    characters: int
    chunks: int


class AskRequest(BaseModel):
    question: str


class Source(BaseModel):

    source: str | None = None
    document_type: str | None = None
    category: str | None = None
    court: str | None = None
    case_name: str | None = None
    year: int | None = None
    citation: str | None = None
    page: int | None = None
    retrieval_source: str | None = None
    rerank_score: float | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]

class QueryClassification(BaseModel):
    category: str
    issue: str
    intent: str
    keywords: list[str]
    requires_user_document: bool

class SessionResponse(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    session_id: str
    question: str