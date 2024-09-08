import logging
from logging.handlers import RotatingFileHandler

from app.config import Config


def setup_logging(app):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handler = RotatingFileHandler("/tmp/app.log", maxBytes=10000, backupCount=1)
    handler.setLevel(Config.LOGGING_LEVEL)
    handler.setFormatter(logging.Formatter(log_format))
    app.logger.addHandler(handler)
    app.logger.setLevel(Config.LOGGING_LEVEL)
