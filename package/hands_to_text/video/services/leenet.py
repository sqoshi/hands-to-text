from typing import Optional

import cv2
import mediapipe as mp
import torch

from hands_to_text.video.images import new_classed_hand_box
from hands_to_text.video.models import ClassedHandBox
from hands_to_text.video.services.abstract import ModelService

# import uuid


class LeeNetModelService(ModelService):
    def __init__(self, path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load(path)
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7
        )

    def _load(self, path: str):
        model = torch.load(path, map_location=self.device)
        model.eval()
        return model

    def preprocess(self, hand_img):
        """Preprocess the hand image for CNN input."""
        hand_img_resized = cv2.resize(hand_img, (28, 28))
        hand_img_gray = cv2.cvtColor(hand_img_resized, cv2.COLOR_BGR2GRAY)
        hand_img_normalized = hand_img_gray / 255.0
        hand_img_tensor = (
            torch.tensor(hand_img_normalized, dtype=torch.float32)
            .unsqueeze(0)
            .unsqueeze(0)
        )
        print(hand_img_normalized.dtype)
        return hand_img_tensor.to(self.device)

    def detect_hand(self, frame, margin_percentage=0.3):
        """Detect the hand region in the frame using MediaPipe."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = frame.shape
                x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
                y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
                x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
                y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

                margin_x = int((x_max - x_min) * margin_percentage)
                margin_y = int((y_max - y_min) * margin_percentage)

                x_min = max(0, x_min - margin_x)
                y_min = max(0, y_min - margin_y)
                x_max = min(w, x_max + margin_x)
                y_max = min(h, y_max + margin_y)

                hand_region = frame[y_min:y_max, x_min:x_max]

                return hand_region, (x_min, y_min, x_max, y_max)

        return None, None

    def predict(self, frame) -> Optional[ClassedHandBox]:
        """Predict the class for the detected hand using CNN."""
        hand_region, box_coords = self.detect_hand(frame)
        if hand_region is not None:
            preprocessed_hand = self.preprocess(hand_region)
            with torch.no_grad():
                output = self.model(preprocessed_hand)
                _, predicted_class = torch.max(output, 1)
            class_name = self.letter(predicted_class.item())

            return new_classed_hand_box(*box_coords, class_name)
        return None

    def letter(self, number: int):
        """Convert CNN model prediction (0-25) to alphabet letter (excluding 'J')."""
        if 1 <= number <= 9:
            return chr(number + ord("A") - 1)
        return chr(number + ord("A"))
