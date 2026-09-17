import os

from src.create_app import create_app
from src.extensions import socketio


app = create_app()


if __name__ == "__main__":
    debug_mode = os.getenv(
        "FLASK_DEBUG",
        "false",
    ).lower() == "true"

    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=debug_mode,
    )