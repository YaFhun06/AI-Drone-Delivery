from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config import Config
from src.infrastructure.databases.base import db

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    with app.app_context():
        from src.infrastructure.models import user_model, role_model

    from src.api.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from src.error_handler import register_error_handlers
    from src.logging import setup_logging

    register_error_handlers(app)
    setup_logging(app)

    return app