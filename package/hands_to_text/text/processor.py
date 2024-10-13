from typing import List, Optional

from .abstract import TextProcessingStrategy
from .strategy import FilterContiniousSymbolsStrategy, RemoveRepetitionsStrategy


class TextProcessor:
    def __init__(self, strategies: Optional[List[TextProcessingStrategy]] = None):
        if strategies is None:
            strategies = [
                FilterContiniousSymbolsStrategy(),
                RemoveRepetitionsStrategy(),
            ]
        self.strategies = strategies

    def __str__(self):
        return f"{', '.join([str(_) for _ in self.strategies])}"

    def process(self, text: str) -> str:
        for strategy in self.strategies:
            text = strategy.process(text)
        return text
