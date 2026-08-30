from src.infrastructure.models.package_pickup_model import PackagePickupModel
from src.infrastructure.databases.base import db


class PackagePickupRepository:

    def get_all(self):
        return PackagePickupModel.query.all()

    def find_by_id(self, pickup_id):
        return PackagePickupModel.query.get(pickup_id)

    def find_by_package_id(self, package_id):
        return PackagePickupModel.query.filter_by(
            package_id=package_id
        ).first()

    def create_pickup(
        self,
        package_id,
        station_id,
        picked_up_by,
        picked_up_at=None
    ):
        pickup = PackagePickupModel(
            package_id=package_id,
            station_id=station_id,
            picked_up_by=picked_up_by
        )

        if picked_up_at is not None:
            pickup.picked_up_at = picked_up_at

        db.session.add(pickup)
        db.session.commit()

        return pickup