import itertools
import logging
from typing import List

import fuzzy
import openai
import textdistance
import wordninja
from autocorrect import Speller
from transformers import pipeline

from .abstract import TextProcessingStrategy


class PhoneticCorrectionStrategy(TextProcessingStrategy):
    """
    A strategy that uses phonetic algorithms to correct letters based on their phonetic sound.
    """

    def __init__(self):
        self.soundex = fuzzy.Soundex(5)

    def process(self, text: str) -> str:
        try:
            words = text.split()
            corrected_words = [self.soundex(word) for word in words]
            return " ".join(corrected_words)
        except Exception:
            return text


class KeepRepeatedSymbolsStrategy(TextProcessingStrategy):
    """
    A strategy to remove symbols that do not repeat continuously for
    a specified number of times (N).
    Only symbols that repeat N or more times will be kept.
    """

    def process(self, text: str, min_reps: int = 3) -> str:
        result = ""
        current_symbol = None
        current_count = 0

        for symbol in text:
            if symbol == current_symbol:
                current_count += 1
            else:
                if current_count >= min_reps:
                    result += current_symbol * current_count
                current_symbol = symbol
                current_count = 1

        if current_symbol and current_count >= min_reps:
            result += current_symbol * current_count

        return result


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


class AutoCorrectionStrategy(TextProcessingStrategy):
    """
    A strategy to autocorrect the text.
    For example, "aaabbbbcc" becomes "abc".
    """

    def __init__(self):
        self.speller = Speller("en")

    def process(self, text: str) -> str:
        return self.speller(text)


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
                if current_symbol and current_count < min_reps:
                    filtered_string += current_symbol * current_count
                current_symbol = symbol
                current_count = 1

        if current_symbol and current_count < min_reps:
            filtered_string += current_symbol * current_count

        return filtered_string


class LeverageLanguageModelStrategy(TextProcessingStrategy):
    """
    A strategy that uses a language model (like GPT-2) to correct noisy sequences.
    """

    def __init__(self, model_name: str = "gpt2"):
        # set_seed(42)
        self.model = pipeline("text-generation", model=model_name)
        # self.model = pipeline("text2text-generation", model="t5-base")
        # self.model = pipeline("text2text-generation", model="t5-small")  # or t5-base, t5-large
        # self.model = pipeline("text-generation", model="gpt3.5-turbo", token="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")
        # self.model = pipeline("text-generation", model="facebook/bart-large-cnn")
        # self.model = pipeline("text2text-generation", model=model_name)
        # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
        # model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
        # self.model.pipeline = pipeline(
        #     "text-generation", model="meta-llama/Meta-Llama-3.1-8B", device_map="auto", token="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"
        # )

    def process(self, text: str) -> str:
        generated = self.model(
            f"Please correct the following text: '{text}'", max_length=250
        )
        corrected_text = str(generated)
        return corrected_text


class LevenshteinCorrectionStrategy(TextProcessingStrategy):
    """
    A strategy that uses Levenshtein distance to correct words.
    """

    def __init__(self, word_corpus: List):
        self.word_corpus = word_corpus

    def process(self, text: str) -> str:
        words = text.split()
        corrected_words = []
        for word in words:
            closest_word = min(
                self.word_corpus, key=lambda w: textdistance.levenshtein(word, w)
            )
            corrected_words.append(closest_word)
        return " ".join(corrected_words)


class MajorityVoteStrategy(TextProcessingStrategy):
    """
    Smooths sequences by using a sliding window and taking the most frequent letter
    in the window to reduce noise.

    Example (with window_size=3):
    Input:  "HHHHHEEELLLLOOOO"
    Output: "HHHHHEEELLOOOO"
    """

    def process(self, text: str, window_size: int = 3) -> str:
        if not text:
            return ""
        smoothed_text = []
        for i in range(len(text)):
            start = max(0, i - window_size // 2)
            end = min(len(text), i + window_size // 2 + 1)
            window = text[start:end]
            smoothed_text.append(max(set(window), key=window.count))
        return "".join(smoothed_text)


class WordSegmentationStrategy(TextProcessingStrategy):
    """
    A strategy to split continuous text into words using word segmentation.
    """

    def process(self, text: str) -> str:
        return " ".join(wordninja.split(text))


class ChatG4FStrategy(TextProcessingStrategy):
    def __init__(self, model_name="gpt-3.5-turbo"):
        from g4f.client import Client

        self.client = Client()
        self.model_name = model_name

    def process(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": f"Correct noised text from captured frames to readable sentence: '{text}'",
                }
            ],
        )
        return response.choices[0].message.content


class ChatGPTStrategy(TextProcessingStrategy):
    def __init__(self, api_key: str, model_name="gpt-4o"):
        self.client = openai.Client(api_key=api_key)
        openai.api_key = api_key
        self.model_name = model_name
        self.last_input = None
        self.last_response = None

    def process(self, text: str) -> str:
        if not text.strip():
            return ""
        if self.last_input == text:
            return self.last_response.choices[0].message.content
        self.last_input = text

        self.last_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": f"Transform ASL letters sequence to readable sentence and you must send only result sentence: {text}",
                }
            ],
        )
        logging.debug("chat response %s", self.last_response)
        return self.last_response.choices[0].message.content


def get_all_strategies():
    return TextProcessingStrategy.__subclasses__()


def get_startegies_perms() -> List[List[TextProcessingStrategy]]:
    return [
        list(combo)
        for length in range(1, len(get_all_strategies()) + 1)
        for combo in itertools.permutations(get_all_strategies(), length)
    ]
