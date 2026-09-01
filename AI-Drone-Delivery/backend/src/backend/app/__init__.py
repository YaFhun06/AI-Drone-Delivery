from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dronedelivery.sql'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)

    # Load toàn bộ models để ghi nhận đầy đủ Foreign Keys
    import app.models

    # Đăng ký blueprint
    from app.routes.order_routers import order_bp
    flask_app.register_blueprint(order_bp, url_prefix='/api')

    return flask_app