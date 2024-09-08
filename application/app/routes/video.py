from flask import Blueprint, Response, current_app, jsonify, render_template

from app.utils.camera import CameraManager
from app.utils.frames import generate_frames

video_bp = Blueprint("video", __name__)


@video_bp.route("/")
def index():
    return render_template("index.html")


@video_bp.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@video_bp.route("/stop_camera", methods=["POST"])
def stop_camera():
    success = CameraManager.stop()
    if not success:
        return jsonify({"status": "error", "message": "Cannot close camera"})
    return jsonify({"status": "success"})


@video_bp.route("/start_camera", methods=["POST"])
def start_camera():
    success = CameraManager.start()
    if not success:
        return jsonify({"status": "error", "message": "Cannot open camera"})
    return jsonify({"status": "success"})
