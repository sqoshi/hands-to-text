from flask import Blueprint, jsonify, request

from app.utils.chat_client import ChatClient

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/send_chat", methods=["POST"])
def send_chat():
    data = request.get_json()
    text = data.get("text", "")
    response = ChatClient.send_message(text)
    if response.get("status") == "success":
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": response.get("message")})


@chat_bp.route("/get_chat", methods=["GET"])
def get_chat():
    return jsonify({"chat": ChatClient.get_history()})
