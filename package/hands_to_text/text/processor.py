from typing import List, Optional
from .abstract import TextProcessingStrategy
from .strategy import RemoveRepetitionsStrategy, FilterContiniousSymbolsStrategy


class TextProcessor:
    def __init__(
        self,
        strategies: Optional[List[TextProcessingStrategy]] = (
            RemoveRepetitionsStrategy,
            FilterContiniousSymbolsStrategy,
        ),
    ):
        self.strategies = strategies

    def process(self, text: str) -> str:
        for strategy in self.strategies:
            text = strategy.process(text)
        return text
