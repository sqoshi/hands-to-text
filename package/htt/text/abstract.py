from abc import ABC, abstractmethod


class TextProcessingStrategy(ABC):
    @abstractmethod
    def process(self, text: str) -> str:
        pass
