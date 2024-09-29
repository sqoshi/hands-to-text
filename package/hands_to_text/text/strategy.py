from autocorrect import Speller
from transformers import pipeline, set_seed

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
                if current_count >= min_reps:
                    filtered_string += current_symbol * current_count
                current_symbol = symbol
                current_count = 1
        if current_count >= min_reps:
            filtered_string += current_symbol * current_count

        return filtered_string


class LeverageLanguageModelStrategy(TextProcessingStrategy):
    """
    A strategy that uses a language model (like GPT-2) to correct noisy sequences.
    """

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        set_seed(42)
        # self.model = pipeline("text-generation", model="gpt3.5-turbo", token="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")
        self.model = pipeline("text-generation", model="facebook/bart-large-cnn")
        # self.model = pipeline("text2text-generation", model=model_name)
        self.model = pipeline("text-generation", model="gpt2")
        # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
        # model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
        # self.model.pipeline = pipeline(
        #     "text-generation", model="meta-llama/Meta-Llama-3.1-8B", device_map="auto", token="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"
        # )

    def process(self, text: str) -> str:
        generated = self.model(f"Correct sentences: '{text}'", max_length=250)
        corrected_text = str(generated)
        return corrected_text


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


# from hmmlearn import hmm
# class ProbabilisticSmoothingStrategy(TextProcessingStrategy):
#     """
#     A strategy using Hidden Markov Model (HMM) for probabilistic smoothing.
#     """

#     def __init__(self):
#         self.model = self._train_hmm_model()

#     def _train_hmm_model(self):
#         model = hmm.MultinomialHMM(n_components=26)
#         # Fake training data (alphabet as sequence, needs real training)
#         X = np.array([[i] for i in range(26)] * 10)  # Simplified
#         model.fit(X)
#         return model

#     def process(self, text: str) -> str:
#         # Map each character to an integer for HMM
#         letter_to_int = {chr(i + 65): i for i in range(26)}  # A-Z
#         int_to_letter = {i: chr(i + 65) for i in range(26)}

#         int_sequence = np.array([[letter_to_int[char]] for char in text if char in letter_to_int])

#         # Predict the most likely sequence
#         logprob, predicted_sequence = self.model.decode(int_sequence, algorithm="viterbi")

#         # Convert back to letters
#         smoothed_text = ''.join([int_to_letter[i] for i in predicted_sequence])

#         return smoothed_text
