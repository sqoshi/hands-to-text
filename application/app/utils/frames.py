from threading import Lock

import cv2
from flask import current_app
from hands_to_text.video.images import draw_classbox, process_frame

text_lock = Lock()


def generate_frames():
    while True:
        if (
            current_app.camera_manager.cap is None
            or not current_app.camera_manager.cap.isOpened()
        ):
            current_app.logger.error("Camera not available")
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + b""
            continue

        success, frame = current_app.camera_manager.cap.read()
        if not success:
            current_app.logger.error("Failed to capture frame")
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + b""
            continue

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        chbox = process_frame(
            img, current_app.config["MODEL"], current_app.config["HANDS"]
        )

        if chbox:
            draw_classbox(img, chbox)
            with text_lock:
                current_app.config["RECOGNIZED_TEXT"] += chbox.class_name
                current_app.logger.info(f"Appended to text: {chbox.class_name}")

        ret, buffer = cv2.imencode(".jpg", img)
        if not ret:
            current_app.logger.error("Failed to convert frame to JPEG")
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + b""
            continue

        frame = buffer.tobytes()
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
