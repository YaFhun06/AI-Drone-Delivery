import pytest

from src.infrastructure.databases.base import db

from src.infrastructure.models.customer_model import CustomerModel
from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.models.package_model import PackageModel
from src.infrastructure.models.package_status_history_model import (
    PackageStatusHistoryModel
)

from src.services.package_status_service import PackageStatusService

from src.domain.exceptions import (
    PackageNotFoundError,
    InvalidPackageStatusError,
)


def create_test_package():
    customer = CustomerModel(
        full_name="Test Customer",
        phone="0123456789"
    )

    db.session.add(customer)
    db.session.commit()

    order = OrderModel(
        customer_id=customer.id,
        status="PENDING"
    )

    db.session.add(order)
    db.session.commit()

    package = PackageModel(
        order_id=order.id,
        weight=1.5,
        description="Test Package",
        status="RECEIVED"
    )

    db.session.add(package)
    db.session.commit()

    return package


def test_update_status_received_to_processing(app):
    with app.app_context():
        package = create_test_package()

        service = PackageStatusService()

        updated_package = service.update_status(
            package.id,
            "PROCESSING"
        )

        assert updated_package.status == "PROCESSING"

        history = PackageStatusHistoryModel.query.filter_by(
            package_id=package.id
        ).first()

        assert history is not None
        assert history.status == "PROCESSING"


def test_update_status_package_not_found(app):
    with app.app_context():
        service = PackageStatusService()

        with pytest.raises(PackageNotFoundError):
            service.update_status(
                999,
                "PROCESSING"
            )


def test_update_status_invalid_status(app):
    with app.app_context():
        package = create_test_package()

        service = PackageStatusService()

        with pytest.raises(InvalidPackageStatusError):
            service.update_status(
                package.id,
                "INVALID_STATUS"
            )


def test_update_status_wrong_transition(app):
    with app.app_context():
        package = create_test_package()

        service = PackageStatusService()

        with pytest.raises(InvalidPackageStatusError):
            service.update_status(
                package.id,
                "DISPATCHED"
            )