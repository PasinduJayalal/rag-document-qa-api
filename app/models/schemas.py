from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    context_chunks: list[str]


class IngestResponse(BaseModel):
    message: str
    filename: str
    chunks_stored: int