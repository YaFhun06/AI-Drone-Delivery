from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Đăng ký Blueprint Address
    from app.routes.address import address_bp
    app.register_blueprint(address_bp)

    # Lệnh seed-db
    @app.cli.command("seed-db")
    def seed_db():
        from app.models.role import Role
        from app.models.station import Station

        roles_data = ['Admin', 'Customer', 'Operator', 'Dispatcher', 'Logistics Manager']
        for role_name in roles_data:
            if not Role.query.filter_by(role_name=role_name).first():
                db.session.add(Role(role_name=role_name))

        stations_data = [
            {"name": "Trạm Tân Bình", "capacity": 10, "latitude": 10.8012, "longitude": 106.6578, "status": "ACTIVE"},
            {"name": "Trạm Quận 1", "capacity": 15, "latitude": 10.7769, "longitude": 106.7009, "status": "ACTIVE"},
            {"name": "Trạm Thủ Đức", "capacity": 8, "latitude": 10.8505, "longitude": 106.7719, "status": "ACTIVE"}
        ]
        for st in stations_data:
            if not Station.query.filter_by(name=st["name"]).first():
                db.session.add(Station(**st))

        db.session.commit()
        print("Seed du lieu thanh cong!")

    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Đăng ký Blueprints
    from app.routes.address import address_bp
    from app.routes.customer import customer_bp
    
    app.register_blueprint(address_bp)
    app.register_blueprint(customer_bp)

    return app