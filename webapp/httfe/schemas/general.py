from typing import Optional

from pydantic import BaseModel


class GeneralResponse(BaseModel):
    status: str
    message: Optional[str] = None
