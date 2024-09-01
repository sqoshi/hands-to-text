import logging
import os
import warnings
from logging.handlers import RotatingFileHandler
from threading import Lock

import cv2
from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS
from g4f.client import Client
from hands_to_text.text import TextProcessor
from hands_to_text.video import draw_classbox, process_frame, read_hands_models

warnings.filterwarnings(
    "ignore", category=DeprecationWarning, module="google.protobuf.symbol_database"
)
warnings.filterwarnings(
    "ignore", category=UserWarning, module="google.protobuf.symbol_database"
)

text_lock = Lock()
app = Flask(__name__)
CORS(app)

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

if not app.debug:
    handler = RotatingFileHandler("/tmp/app.log", maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(log_format))
    app.logger.addHandler(handler)

app.logger.setLevel(logging.DEBUG)


def generate_frames():
    while True:
        if app.config["CAP"] is None or not app.config["CAP"].isOpened():
            app.logger.error("Camera not available")
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + b""
            continue

        success, frame = app.config["CAP"].read()
        if not success:
            app.logger.error("Failed to capture frame")
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + b""
            continue

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        chbox = process_frame(img, app.config["MODEL"], app.config["HANDS"])

        if chbox:
            draw_classbox(img, chbox)
            with text_lock:
                app.config["RECOGNIZED_TEXT"] += chbox.class_name
                app.logger.info(f"Appended to file: {chbox.class_name}")

        ret, buffer = cv2.imencode(".jpg", img)
        if not ret:
            app.logger.error("Failed to convert frame to JPEG")
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + b""
            continue

        frame = buffer.tobytes()
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/stop_camera", methods=["POST"])
def stop_camera():
    if app.config["CAP"] is not None:
        app.config["CAP"].release()
        app.config["CAP"] = None
    if app.config["CAP"] and app.config["CAP"].isOpened():
        return jsonify({"status": "error", "message": "Cannot close camera"})
    return jsonify({"status": "success"})


@app.route("/start_camera", methods=["POST"])
def start_camera():
    if app.config["CAP"] is not None:
        app.config["CAP"].release()
    app.config["CAP"] = cv2.VideoCapture(0)
    if not app.config["CAP"].isOpened():
        return jsonify({"status": "error", "message": "Cannot open camera"})
    return jsonify({"status": "success"})


@app.route("/get_text_corrected", methods=["GET"])
def get_text_corrected():
    return jsonify(
        {"text": app.config["TEXT_PROCESSOR"].process(app.config["RECOGNIZED_TEXT"])}
    )


@app.route("/get_text", methods=["GET"])
def get_text():
    return jsonify({"text": app.config["RECOGNIZED_TEXT"]})


@app.route("/reset_text", methods=["POST"])
def reset_text():
    app.config["RECOGNIZED_TEXT"] = ""
    return jsonify({"status": "success"})


@app.route("/send_chat", methods=["POST"])
def send_chat():
    data = request.get_json()
    text = data.get("text", "")
    app.config["CHAT_HISTORY"].append(f"You: {text}")
    client = Client()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
        )
        assistant_response = response.choices[0].message.content
        app.logger.debug("Assistant response: %s", assistant_response)
        app.config["CHAT_HISTORY"].append(f"Assistant: {assistant_response}")
        return jsonify({"status": "success"})
    except Exception as e:
        app.logger.error("Error during chat completion: %s", e)
        return jsonify(
            {
                "status": "error",
                "message": "Failed to get a response from the assistant",
            }
        )


@app.route("/get_chat", methods=["GET"])
def get_chat():
    return jsonify({"chat": "\n".join(app.config["CHAT_HISTORY"])})


with app.app_context():
    app.config["CAP"] = None
    app.config["CHAT_HISTORY"] = []
    app.config["RECOGNIZED_TEXT"] = ""
    app.config["TEXT_PROCESSOR"] = TextProcessor()
    app.config["MODEL"], app.config["HANDS"] = read_hands_models(
        os.getenv("HANDS_MODEL_PATH", "../models/model.pickle")
    )


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
