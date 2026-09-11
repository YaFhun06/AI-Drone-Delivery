import pytest

from src.infrastructure.databases.base import db
from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.station_model import StationModel
from src.infrastructure.models.package_receipt_model import (
    PackageReceiptModel
)
from src.services.package_receipt_service import PackageReceiptService
from src.domain.exceptions import (
    StationNotFoundError,
    PackageAlreadyReceivedError,
    PackageReceiptNotFoundError,
)


def create_test_data():
    role = RoleModel(
        name="TEST_OPERATOR",
        description="Test station operator"
    )
    db.session.add(role)
    db.session.commit()

    user = UserModel(
        full_name="Test Operator",
        email="operator@test.com",
        password_hash="test_password",
        role_id=role.id
    )
    db.session.add(user)

    station = StationModel(
        name="Test Station",
        capacity=100,
        latitude=10.762622,
        longitude=106.660172,
        status="ACTIVE"
    )
    db.session.add(station)
    db.session.commit()

    return user, station


def test_create_receipt_success(app):
    with app.app_context():
        user, station = create_test_data()

        service = PackageReceiptService()

        receipt = service.create_receipt(
            package_id=1,
            station_id=station.id,
            received_by=user.id
        )

        assert receipt.id is not None
        assert receipt.package_id == 1
        assert receipt.station_id == station.id
        assert receipt.received_by == user.id


def test_create_receipt_station_not_found(app):
    with app.app_context():
        service = PackageReceiptService()

        with pytest.raises(StationNotFoundError):
            service.create_receipt(
                package_id=1,
                station_id=999,
                received_by=1
            )


def test_create_duplicate_receipt(app):
    with app.app_context():
        user, station = create_test_data()

        service = PackageReceiptService()

        service.create_receipt(
            package_id=1,
            station_id=station.id,
            received_by=user.id
        )

        with pytest.raises(PackageAlreadyReceivedError):
            service.create_receipt(
                package_id=1,
                station_id=station.id,
                received_by=user.id
            )


def test_get_receipt_not_found(app):
    with app.app_context():
        service = PackageReceiptService()

        with pytest.raises(PackageReceiptNotFoundError):
            service.get_receipt(999)