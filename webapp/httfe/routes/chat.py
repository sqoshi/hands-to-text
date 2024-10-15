from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from httfe.schemas.chat import ChatHistoryResponse, ChatMessage, ChatResponse
from httfe.services.chat import ChatService, get_chat_srv

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def send_chat(
    message: ChatMessage, chat_service: Annotated[ChatService, Depends(get_chat_srv)]
):
    try:
        print("chat route called")
        await chat_service.send_chat(message.text)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return ChatResponse(status="success")


@router.get("/", response_model=ChatHistoryResponse)
async def get_chat(chat_service: Annotated[ChatService, Depends(get_chat_srv)]):
    return ChatHistoryResponse(status="success", chat=chat_service.get_history())
