from flask import c

from app import create_app
from app.utils.logging import setup_logging

app = create_app()
setup_logging(app)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, threaded=False)
