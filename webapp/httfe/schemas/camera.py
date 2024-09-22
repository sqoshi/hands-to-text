from typing import Optional
from pydantic import BaseModel


class CameraResponse(BaseModel):
    status: str
    message: Optional[str] = None
