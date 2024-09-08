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

        return filtered_string


class LeverageLanguageModelStrategy(TextProcessingStrategy):
    """
    A strategy that uses a language model (like GPT-2) to correct noisy sequences.
    """

    def __init__(self, model_name: str = "gpt2"):
        self.model = pipeline("text-generation", model=model_name)

    def process(self, text: str) -> str:
        prompt = (
            "The following sequence of letters was collected from sign language "
            "classification in video frames. The sequence contains repeated letters "
            "due to frame-by-frame detection. Please correct the sequence into a valid word or phrase. "
            "For example, 'HHHHHEEELLLLOOOO' should become 'HELLO'. Correct this sequence: "
            f"'{text}'"
        )
        generated = self.model(prompt, max_length=50, num_return_sequences=1)
        corrected_text = generated[0]["generated_text"].strip()
        return corrected_text


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
