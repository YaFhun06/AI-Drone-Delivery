from src.infrastructure.models.package_model import PackageModel
from src.infrastructure.databases.base import db


class PackageRepository:
    def create(self, order_id, weight, dimensions=None, description=None):
        package = PackageModel(
            order_id=order_id, weight=weight,
            dimensions=dimensions, description=description,
        )
        db.session.add(package)
        db.session.commit()
        return package

    def find_by_order_id(self, order_id):
        return PackageModel.query.filter_by(order_id=order_id).all()