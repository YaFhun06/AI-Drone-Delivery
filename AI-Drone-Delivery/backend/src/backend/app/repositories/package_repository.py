from app import db
from app.models.package import Package

class PackageRepository:
    @staticmethod
    def create(package):
        db.session.add(package)
        db.session.commit()
        return package

    @staticmethod
    def get_by_order_id(order_id):
        return Package.query.filter_by(order_id=order_id).all()