from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from src.config import Config
from src.infrastructure.databases.base import db
from src.extensions import socketio
from src.sockets import register_socket_events


migrate = Migrate()
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Dự phòng: Nếu file .env không đọc được thì tự gán DATABASE_URL
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "postgresql://postgres.rotdzkcmwvvqulbvytpd:"
            "Congnghephanmem@aws-0-ap-southeast-1.pooler.supabase.com:"
            "6543/postgres"
        )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True
    )

    # SocketIO
    socketio.init_app(app)
    register_socket_events(socketio)

    # Import Models
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
            notification_model,
            drone_model,
            package_receipt_model,
        )

    # Đăng ký Controllers
    from src.api.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from src.api.controllers.management_controller import management_bp
    app.register_blueprint(management_bp)

    from src.api.controllers.role_controller import role_bp
    app.register_blueprint(role_bp)

    from src.api.controllers.address_controller import address_bp
    app.register_blueprint(address_bp)

    from src.api.controllers.customer_controller import customer_bp
    app.register_blueprint(customer_bp)

    from src.api.controllers.station_controller import station_bp
    app.register_blueprint(station_bp)

    from src.api.controllers.eta_controller import eta_bp
    app.register_blueprint(eta_bp)

    from src.api.controllers.chatbot_controller import chatbot_bp
    app.register_blueprint(chatbot_bp)

    from src.api.controllers.delivery_summary_controller import (
        delivery_summary_bp
    )
    app.register_blueprint(delivery_summary_bp)

    from src.api.controllers.order_controller import order_bp
    app.register_blueprint(order_bp)

    from src.api.controllers.analytics_controller import analytics_bp
    app.register_blueprint(analytics_bp)

    from src.api.controllers.health_controller import health_bp
    app.register_blueprint(health_bp)

    from src.api.controllers.package_status_controller import package_status_bp
    app.register_blueprint(package_status_bp)

    # Drone Controller
    try:
        from src.api.controllers.drone_controller import drone_bp
        app.register_blueprint(drone_bp)
    except ImportError:
        pass

    # Error Handler + Logging
    from src.error_handler import register_error_handlers
    from src.logging import setup_logging

    register_error_handlers(app)
    setup_logging(app)

    return app