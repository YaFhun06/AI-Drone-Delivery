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
        from src.infrastructure.models import user_model, role_model, auth_function_model, auth_role_function_model, address_model, customer_model

    from src.api.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    from src.api.controllers.role_controller import role_bp
    app.register_blueprint(role_bp)

    from src.api.controllers.address_controller import address_bp
    app.register_blueprint(address_bp)
    from src.api.controllers.customer_controller import customer_bp
    app.register_blueprint(customer_bp)


    return app