import uuid

from httfe.services.utils import singleton

from hands_to_text.text import (
    MajorityVoteStrategy,
    RemoveRepetitionsStrategy,
    TextProcessor,
)


@singleton
class TextService:
    def __init__(self):
        self.myid = uuid.uuid4()
        self.processor = TextProcessor(
            strategies=[RemoveRepetitionsStrategy(), MajorityVoteStrategy()]
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
