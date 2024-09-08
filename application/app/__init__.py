import os

from flask import Flask
from flask_cors import CORS
from hands_to_text.text import TextProcessor
from hands_to_text.video.images import read_hands_models

from .config import Config
from .utils.camera import CameraManager
from .utils.chat_client import ChatClient


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Initialize app configuration
    app.config["RECOGNIZED_TEXT"] = ""  # Ensure this key is initialized
    app.config["CORRECTED_TEXT"] = ""  # Ensure this key is initialized
    app.config["CHAT_HISTORY"] = []  # Initialize chat history
    app.config["MODEL"], app.config["HANDS"] = read_hands_models(
        os.getenv("HANDS_MODEL_PATH", "../models/model.pickle")
    )
    # Initialize resources
    app.camera_manager = CameraManager()
    app.text_processor = TextProcessor()
    app.chat_client = ChatClient()

    # Register blueprints
    from .routes.chat import chat_bp
    from .routes.text import text_bp
    from .routes.video import video_bp

    app.register_blueprint(video_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(text_bp)

    return app
