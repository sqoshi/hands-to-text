import asyncio

from g4f.client import Client
from httfe.services.utils import singleton


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
        print("chat sending..")
        # response = self.client.chat.completions.create(
        response = await asyncio.to_thread(
            self.client.chat.completions.create(  # Runs in separate thread
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"Correct noiced text from captured from frames to readable sentence and answear: {text}",
                    }
                ],
            )
        )
        print("chat response", response)
        assistant_response = response.choices[0].message.content
        self.history.append(f"Assistant: {assistant_response}")

    def get_history(self):
        return "\n".join(self.history)


def get_chat_srv() -> ChatService:
    return ChatService()
