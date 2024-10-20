import cv2

from hands_to_text.video.services.abstract import ModelService


class AdaBoostModelService(ModelService):
    def __init__(self, model):
        self.model = model

    def preprocess(self, frame):
        hand_img_resized = cv2.resize(frame, (28, 28))
        hand_img_gray = cv2.cvtColor(hand_img_resized, cv2.COLOR_BGR2GRAY)
        hand_img_flattened = hand_img_gray.flatten()
        return hand_img_flattened.reshape(1, -1)

    def predict(self, frame):
        preprocessed_hand = self.preprocess(frame)
        return self.model.predict(preprocessed_hand)[0]
