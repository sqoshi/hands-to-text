from pydantic import BaseModel


class TextResponse(BaseModel):
    text: str


class TextResetResponse(BaseModel):
    status: str
