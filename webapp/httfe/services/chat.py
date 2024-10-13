import asyncio
import logging

import openai

from httfe.core.config import settings
from httfe.services.utils import singleton


@singleton
class ChatService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_name="gpt-4.0"):
        openai.api_key = settings().chat.key
        self.history = []
        self.model_name = model_name

    async def send_chat(self, text):
        self.history.append(f"You: {text}")
        logging.debug("chat sending..")

        response = await asyncio.to_thread(
            openai.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": f"Answear : {text}",
                    }
                ],
            )
        )
        logging.debug("chat response %s", response)
        assistant_response = response.choices[0].message["content"]
        self.history.append(f"Assistant: {assistant_response}")

    def get_history(self):
        return "\n".join(self.history)


def get_chat_srv() -> ChatService:
    return ChatService()
