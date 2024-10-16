from typing import Annotated

from fastapi import APIRouter, Depends, Query

from httfe.schemas.text import TextResetResponse, TextResponse
from httfe.services.text import TextService, get_text_srv

router = APIRouter()


@router.get("/", response_model=TextResponse)
async def get_text(
    text_service: Annotated[TextService, Depends(get_text_srv)],
    corrected: bool = Query(False),
):
    text = text_service.process_text() if corrected else text_service.recognized_text
    return TextResponse(text=text)


@router.delete("/", response_model=TextResetResponse)
async def reset_text(text_service: Annotated[TextService, Depends(get_text_srv)]):
    text_service.reset_text()
    return TextResetResponse(status="success")
