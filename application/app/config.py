import os


class Config:
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG").upper()
    HANDS_MODEL_PATH = os.getenv("HANDS_MODEL_PATH", "../models/model.pickle")
    # Add more configuration variables as needed
