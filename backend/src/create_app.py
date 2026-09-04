from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config import Config
from src.infrastructure.databases.base import db

migrate = Migrate()
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    with app.app_context():
        from src.infrastructure.models import (
            user_model,
            role_model,
            auth_function_model,
            auth_role_function_model,
            address_model,
            customer_model,
            station_model,
            order_model,
            package_model,
            package_receipt_model,
        )

    from src.api.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    from src.api.controllers.role_controller import role_bp
    app.register_blueprint(role_bp)

    from src.api.controllers.address_controller import address_bp
    app.register_blueprint(address_bp)
    from src.api.controllers.customer_controller import customer_bp
    app.register_blueprint(customer_bp)

    from src.api.controllers.station_controller import station_bp
    app.register_blueprint(station_bp)

    from src.error_handler import register_error_handlers
    from src.logging import setup_logging
    register_error_handlers(app)
    setup_logging(app)

    from src.api.controllers.eta_controller import eta_bp
    app.register_blueprint(eta_bp)

    from src.api.controllers.chatbot_controller import chatbot_bp
    app.register_blueprint(chatbot_bp)

    from src.api.controllers.delivery_summary_controller import delivery_summary_bp
    app.register_blueprint(delivery_summary_bp)

    from src.api.controllers.order_controller import order_bp
    app.register_blueprint(order_bp)
    from src.api.controllers.package_receipt_controller import package_receipt_bp
    app.register_blueprint(package_receipt_bp)

    from src.api.controllers.analytics_controller import analytics_bp
    app.register_blueprint(analytics_bp)

    return app