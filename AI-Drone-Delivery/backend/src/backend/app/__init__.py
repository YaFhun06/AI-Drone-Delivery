from flask import Flask
from app.extensions import db

# Import các Blueprint
from app.routes.drone_routers import drone_bp

# THÊM CÁC DÒNG NÀY: Import trực tiếp các Model để SQLAlchemy nhận diện bảng stations trước
from app.models.station import Station
from app.models.drone import Drone

def create_app():
    app = Flask(__name__)
    
    # Cấu hình chuỗi kết nối DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khởi tạo db
    db.init_app(app)

    # Đăng ký Blueprint
    app.register_blueprint(drone_bp)

    # Tự động tạo bảng dữ liệu
    with app.app_context():
        db.create_all()

    return app