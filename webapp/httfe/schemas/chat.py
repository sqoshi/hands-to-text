from typing import Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    text: str


class ChatResponse(BaseModel):
    status: str
    message: Optional[str] = None


class ChatHistoryResponse(BaseModel):
    status: str
    chat: str
