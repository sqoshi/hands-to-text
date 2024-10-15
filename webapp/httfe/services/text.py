from hands_to_text.text import TextProcessor
from hands_to_text.text.strategy import ChatGPTStrategy

from httfe.core.config import settings
from httfe.services.utils import singleton


@singleton
class TextService:
    def __init__(self):
        self.processor = TextProcessor(
            strategies=[
                ChatGPTStrategy(api_key=settings().chat.key),
            ]
        )
        self.recognized_text = ""

    def process_text(self):
        return self.processor.process(self.recognized_text)

    def update_text(self, text: str):
        self.recognized_text = self.recognized_text + text

    def reset_text(self):
        self.recognized_text = ""


def get_text_srv() -> TextService:
    return TextService()
