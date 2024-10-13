import asyncio
import logging

import openai
from g4f.client import Client

from httfe.core.config import settings
from httfe.services.utils import singleton

openai.api_key = settings.chat.key


@singleton
class ChatService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.history = []
        self.client = Client()

    async def send_chat(self, text):
        self.history.append(f"You: {text}")
        logging.debug("chat sending..")

        response = await asyncio.to_thread(
            openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"Correct noticed text from captured frames to readable sentence and answer: {text}",
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
