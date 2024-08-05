import cv2
from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS
from g4f.client import Client
from htt.general import draw_classbox, process_frame, read_hands_models

app = Flask(__name__)
CORS(app)  # Enable CORS


def generate_frames():
    while app.config["CAP"] is not None and app.config["CAP"].isOpened():
        success, frame = app.config["CAP"].read()
        if not success:
            print("Failed to capture frame")
            continue
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        chbox = process_frame(img, app.config["MODEL"], app.config["HANDS"])
        if chbox:
            draw_classbox(img, chbox)
            app.config["RECOGNIZED_TEXT"] += chbox.class_name
        ret, buffer = cv2.imencode(".jpg", img)
        if not ret:
            print("Failed to convert frame to JPEG")
            continue
        frame = buffer.tobytes()

        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


def remove_repetitions(s: str) -> str:
    if not s:
        return ""
    result = [s[0]]
    for char in s[1:]:
        if char != result[-1]:
            result.append(char)
    return "".join(result)


def filter_continuous_symbols(input_string: str, min_reps: int = 10) -> str:
    filtered_string = ""
    current_symbol = None
    current_count = 0

    for i, symbol in enumerate(input_string):
        if symbol == current_symbol:
            current_count += 1
        else:
            if current_count >= min_reps:
                filtered_string += current_symbol * current_count
            current_symbol = symbol
            current_count = 1
    if current_count >= min_reps:
        filtered_string += current_symbol * current_count

    return remove_repetitions(filtered_string)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


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
    return jsonify({"text": filter_continuous_symbols(app.config["RECOGNIZED_TEXT"])})


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
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
    )
    assistant_response = response.choices[0].message.content
    app.logger.debug("Assistant response: %s", assistant_response)
    app.config["CHAT_HISTORY"].append(f"Assistant: {assistant_response}")
    return jsonify({"status": "success"})


@app.route("/get_chat", methods=["GET"])
def get_chat():
    return jsonify({"chat": "\n".join(app.config["CHAT_HISTORY"])})


with app.app_context():
    app.config["CAP"] = None
    app.config["CHAT_HISTORY"] = []
    app.config["RECOGNIZED_TEXT"] = ""
    app.config["MODEL"], app.config["HANDS"] = read_hands_models(
        "../models/model.pickle"
    )


if __name__ == "__main__":
    app.run(debug=True)
