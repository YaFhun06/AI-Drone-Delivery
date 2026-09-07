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
    # Dự phòng: Nếu file .env không đọc được thì tự gán thẳng chuỗi Supabase vào
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres.rotdzkcmwvvqulbvytpd:Congnghephanmem@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Mở toàn bộ quyền CORS cho Frontend từ cổng 5173
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

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
        )

    # Đăng ký các Controllers
    from src.api.controllers.customer_controller import customer_bp
    app.register_blueprint(customer_bp)

    from src.api.controllers.station_controller import station_bp
    app.register_blueprint(station_bp)

    from src.api.controllers.eta_controller import eta_bp
    app.register_blueprint(eta_bp)

    from src.api.controllers.chatbot_controller import chatbot_bp
    app.register_blueprint(chatbot_bp)

    from src.api.controllers.delivery_summary_controller import delivery_summary_bp
    app.register_blueprint(delivery_summary_bp)

    # Để trần vì trong order_controller.py đã có sẵn "/api/orders"
    from src.api.controllers.order_controller import order_bp
    app.register_blueprint(order_bp)

    # Để trần vì trong analytics_controller.py đã có sẵn "/api/analytics"
    from src.api.controllers.analytics_controller import analytics_bp
    app.register_blueprint(analytics_bp)

    # Đăng ký thêm Drone Controller (bắt buộc để hết lỗi 404 của Quản lý Drone)
    try:
        from src.api.controllers.drone_controller import drone_bp
        app.register_blueprint(drone_bp)
    except ImportError:
        pass

    from src.error_handler import register_error_handlers
    from src.logging import setup_logging
    register_error_handlers(app)
    setup_logging(app)

    return app