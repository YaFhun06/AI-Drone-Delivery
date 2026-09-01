from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Fix chính tả: primary_key=True
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)

def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dronedelivery.sql'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)

    # Nạp các model
    from app.models.order import Order
    from app.models.package import Package

    # Đăng ký blueprint
    from app.routes.order_routers import order_bp
    flask_app.register_blueprint(order_bp, url_prefix='/api')

    return flask_app