from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    filename: str
    characters: int
    chunks: int

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str