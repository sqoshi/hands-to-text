import cv2
from hands_to_text.video.images import draw_classbox
from hands_to_text.video.services.rf import RandomForestModelService

from httfe.core.config import settings
from httfe.services.text import TextService
from httfe.services.utils import singleton


@singleton
class CameraService:
    IMG_HEAD = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.cap = cv2.VideoCapture(settings().device.idx)
        self.model_srv = RandomForestModelService(settings().hands.path)

    def read_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return None
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def start_camera(self):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(settings().device.idx)
        return self.cap.isOpened()

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def generate_frames(self, text_service: TextService):
        while True:
            if self.cap is None or not self.cap.isOpened():
                yield self.IMG_HEAD + b""
                continue

            success, frame = self.cap.read()
            if not success:
                yield self.IMG_HEAD + b""
                continue

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            chbox = self.model_srv.predict(img)

            if chbox:
                draw_classbox(img, chbox)
                text_service.update_text(chbox.class_name)

            ret, buffer = cv2.imencode(".jpg", img)
            if not ret:
                yield self.IMG_HEAD + b""
                continue

            yield (self.IMG_HEAD + buffer.tobytes() + b"\r\n")


def get_cam_srv() -> CameraService:
    return CameraService()
