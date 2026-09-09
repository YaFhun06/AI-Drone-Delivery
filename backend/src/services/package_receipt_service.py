from src.infrastructure.repositories.package_receipt_repository import PackageReceiptRepository
from src.infrastructure.repositories.station_repository import StationRepository

from src.domain.exceptions import (
    StationNotFoundError,
    PackageReceiptNotFoundError,
    PackageAlreadyReceivedError,
)


class PackageReceiptService:
    def __init__(
        self,
        package_receipt_repository: PackageReceiptRepository = None,
        station_repository: StationRepository = None
    ):
        self.package_receipt_repository = (
            package_receipt_repository or PackageReceiptRepository()
        )
        self.station_repository = (
            station_repository or StationRepository()
        )

    def list_receipts(self):
        return self.package_receipt_repository.get_all()

    def get_receipt(self, receipt_id):
        receipt = self.package_receipt_repository.find_by_id(receipt_id)

        if not receipt:
            raise PackageReceiptNotFoundError()

        return receipt

    def create_receipt(
        self,
        package_id,
        station_id,
        received_by,
        received_at=None
    ):
        # Kiểm tra station tồn tại
        station = self.station_repository.find_by_id(station_id)

        if not station:
            raise StationNotFoundError()

        # Kiểm tra package đã được xác nhận trước đó chưa
        existing_receipt = (
            self.package_receipt_repository.find_by_package_id(package_id)
        )

        if existing_receipt:
            raise PackageAlreadyReceivedError()

        return self.package_receipt_repository.create_receipt(
            package_id=package_id,
            station_id=station_id,
            received_by=received_by,
            received_at=received_at
        )