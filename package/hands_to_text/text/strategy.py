from .abstract import TextProcessingStrategy

from transformers import pipeline
from .abstract import TextProcessingStrategy


class RemoveRepetitionsStrategy(TextProcessingStrategy):
    """
    A strategy to remove consecutive repeated characters from the text.
    For example, "aaabbbbcc" becomes "abc".
    """

    def process(self, text: str) -> str:
        if not text:
            return ""
        result = [text[0]]
        for char in text[1:]:
            if char != result[-1]:
                result.append(char)
        return "".join(result)


class FilterContiniousSymbolsStrategy(TextProcessingStrategy):
    """
    A strategy to filter out symbols that appear continuously for
    a number of repetitions greater than or equal to a given threshold.
    """

    def process(self, text: str, min_reps: int = 10) -> str:
        filtered_string = ""
        current_symbol = None
        current_count = 0
        for i, symbol in enumerate(text):
            if symbol == current_symbol:
                current_count += 1
            else:
                if current_count >= min_reps:
                    filtered_string += current_symbol * current_count
                current_symbol = symbol
                current_count = 1
        if current_count >= min_reps:
            filtered_string += current_symbol * current_count

        return


class UseModelStrategy(TextProcessingStrategy):
    """
    A strategy that uses a pre-trained language model for text generation or correction.
    """

    def __init__(self, model_name: str = "gpt-2"):
        self.model = pipeline("text-generation", model=model_name)

    def process(self, text: str) -> str:
        generated = self.model(text, max_length=50, num_return_sequences=1)
        return generated[0]["generated_text"]
