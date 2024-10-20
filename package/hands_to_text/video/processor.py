import cv2

from hands_to_text.video.services.abstract import ModelService


class FramesProcessor:
    def __init__(self, model_service: ModelService):
        self.model_service = model_service

    def process_frame(self, frame):
        return self.model_service.predict(frame)

    def process_video(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        recognized_text = ""
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            chbox = self.process_frame(frame)
            if chbox:
                recognized_text += chbox.class_name
        cap.release()
        return recognized_text
