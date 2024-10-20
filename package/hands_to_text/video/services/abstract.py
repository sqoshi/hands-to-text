from abc import ABC, abstractmethod


class ModelService(ABC):
    def __init__(self, path: str):
        self.model = self._load(path)

    @abstractmethod
    def _load(self, path: str):
        pass

    @abstractmethod
    def preprocess(self, frame):
        pass

    @abstractmethod
    def detect_hand(self, frame):
        pass

    @abstractmethod
    def predict(self, frame):
        pass

    @abstractmethod
    def letter(self, number: int):
        pass
