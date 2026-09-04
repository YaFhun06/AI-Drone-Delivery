from src.infrastructure.models.package_receipt_model import PackageReceiptModel
from src.infrastructure.databases.base import db


class PackageReceiptRepository:
    def get_all(self):
        return PackageReceiptModel.query.all()

    def find_by_id(self, receipt_id):
        return PackageReceiptModel.query.get(receipt_id)

    def find_by_package_id(self, package_id):
        return PackageReceiptModel.query.filter_by(
            package_id=package_id
        ).first()

    def create_receipt(
        self,
        package_id,
        station_id,
        received_by,
        received_at=None
    ):
        receipt = PackageReceiptModel(
            package_id=package_id,
            station_id=station_id,
            received_by=received_by
        )

        if received_at is not None:
            receipt.received_at = received_at

        db.session.add(receipt)
        db.session.commit()

        return receipt