import pickle
from typing import Optional

import cv2
import numpy as np

# from mediapipe.python.solutions.drawing_styles import (
# get_default_hand_connections_style,
# get_default_hand_landmarks_style,
# )
# from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.python.solutions.hands import Hands

from hands_to_text.video.images import new_classed_hand_box
from hands_to_text.video.models import ClassedHandBox
from hands_to_text.video.services.abstract import ModelService


class RandomForestModelService(ModelService):
    def __init__(self, path: str):
        self.model = self._load(path)
        self.hands = Hands(
            max_num_hands=1, static_image_mode=True, min_detection_confidence=0.7
        )

    def _load(self, path: str):
        """Load the RandomForest model from the provided model path."""
        with open(path, "rb") as f:
            return pickle.load(f)

    def preprocess(self, frame):
        """Detect hand landmarks and prepare data for RandomForest."""
        data_aux = []
        x_, y_ = [], []
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # draw_landmarks(
                #     frame, hand_landmarks,
                #     HAND_CONNECTIONS,
                #     get_default_hand_landmarks_style(),
                #     get_default_hand_connections_style()
                # )
                for i in range(len(hand_landmarks.landmark)):
                    x_.append(hand_landmarks.landmark[i].x)
                    y_.append(hand_landmarks.landmark[i].y)

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))

            return np.asarray(data_aux), (
                int(min(x_) * W),
                int(min(y_) * H),
                int(max(x_) * W),
                int(max(y_) * H),
            )

        return None, None

    def detect_hand(self, frame):
        """Detect and return hand region (not used explicitly here)."""
        return None

    def predict(self, frame) -> Optional[ClassedHandBox]:
        """Predict the hand gesture using RandomForest."""
        preprocessed_data, box_coords = self.preprocess(frame)

        if preprocessed_data is not None:
            prediction = self.model.predict([preprocessed_data])
            class_name = self.letter(int(prediction[0]))
            return new_classed_hand_box(*box_coords, class_name)

        return None

    def letter(self, number: int):
        """Convert RandomForest prediction (0-25) to alphabet letter."""
        if 0 <= number <= 25:
            return chr(number + ord("A"))  # A to Z
        return None
