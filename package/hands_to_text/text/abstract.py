from abc import ABC, abstractmethod


class TextProcessingStrategy(ABC):
    @abstractmethod
    def process(self, text: str) -> str:
        pass

    def __str__(self):
        return self.__class__.__name__
