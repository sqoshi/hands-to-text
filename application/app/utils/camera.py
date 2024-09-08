import cv2


class CameraManager:
    cap = None

    @classmethod
    def start(cls):
        if cls.cap is not None:
            cls.cap.release()
        cls.cap = cv2.VideoCapture(0)
        return cls.cap.isOpened()

    @classmethod
    def stop(cls):
        if cls.cap is not None:
            cls.cap.release()
            cls.cap = None
        return cls.cap is None or not cls.cap.isOpened()
