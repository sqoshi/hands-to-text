from flask import Blueprint
from flask import current_app as app
from flask import jsonify

text_bp = Blueprint("text", __name__)


@text_bp.route("/get_text_corrected", methods=["GET"])
def get_text_corrected():
    recognized_text = app.text_processor.process(app.config["RECOGNIZED_TEXT"])
    return jsonify({"text": recognized_text})


@text_bp.route("/get_text", methods=["GET"])
def get_text():
    return jsonify({"text": app.config["RECOGNIZED_TEXT"]})


@text_bp.route("/reset_text", methods=["POST"])
def reset_text():
    app.config["RECOGNIZED_TEXT"] = ""
    return jsonify({"status": "success"})
