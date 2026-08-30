from src.infrastructure.repositories.package_pickup_repository import PackagePickupRepository
from src.infrastructure.repositories.station_repository import StationRepository

from src.domain.exceptions import (
    StationNotFoundError,
    PackagePickupNotFoundError,
    PackageAlreadyPickedUpError,
)


class PackagePickupService:
    def __init__(
        self,
        package_pickup_repository: PackagePickupRepository = None,
        station_repository: StationRepository = None
    ):
        self.package_pickup_repository = (
            package_pickup_repository or PackagePickupRepository()
        )
        self.station_repository = (
            station_repository or StationRepository()
        )

    def list_pickups(self):
        return self.package_pickup_repository.get_all()

    def get_pickup(self, pickup_id):
        pickup = self.package_pickup_repository.find_by_id(pickup_id)

        if not pickup:
            raise PackagePickupNotFoundError()

        return pickup

    def create_pickup(
        self,
        package_id,
        station_id,
        picked_up_by,
        picked_up_at=None
    ):
        # Kiểm tra station tồn tại
        station = self.station_repository.find_by_id(station_id)

        if not station:
            raise StationNotFoundError()

        # Kiểm tra package đã được pickup trước đó chưa
        existing_pickup = (
            self.package_pickup_repository.find_by_package_id(package_id)
        )

        if existing_pickup:
            raise PackageAlreadyPickedUpError()

        return self.package_pickup_repository.create_pickup(
            package_id=package_id,
            station_id=station_id,
            picked_up_by=picked_up_by,
            picked_up_at=picked_up_at
        )