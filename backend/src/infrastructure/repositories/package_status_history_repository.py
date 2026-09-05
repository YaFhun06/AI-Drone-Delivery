from src.infrastructure.models.package_status_history_model import (
    PackageStatusHistoryModel
)
from src.infrastructure.databases.base import db


class PackageStatusHistoryRepository:

    def create(self, package_id, status):
        history = PackageStatusHistoryModel(
            package_id=package_id,
            status=status
        )

        db.session.add(history)
        db.session.commit()

        return history

    def find_by_package_id(self, package_id):
        return (
            PackageStatusHistoryModel.query
            .filter_by(package_id=package_id)
            .order_by(PackageStatusHistoryModel.created_at.asc())
            .all()
        )