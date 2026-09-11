import pytest
from datetime import datetime, timedelta

from src.infrastructure.databases.base import db

from src.infrastructure.models.customer_model import CustomerModel
from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.models.package_model import PackageModel
from src.infrastructure.models.package_status_history_model import (
    PackageStatusHistoryModel
)

from src.services.package_timeline_service import (
    PackageTimelineService
)

from src.domain.exceptions import PackageNotFoundError


def create_test_package():
    customer = CustomerModel(
        full_name="Timeline Test Customer",
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
        description="Timeline Test Package",
        status="RECEIVED"
    )

    db.session.add(package)
    db.session.commit()

    return package


def test_get_timeline_success(app):
    with app.app_context():
        package = create_test_package()

        time_1 = datetime.utcnow()
        time_2 = time_1 + timedelta(minutes=5)

        history_1 = PackageStatusHistoryModel(
            package_id=package.id,
            status="PROCESSING",
            created_at=time_1
        )

        history_2 = PackageStatusHistoryModel(
            package_id=package.id,
            status="DISPATCHED",
            created_at=time_2
        )

        db.session.add(history_1)
        db.session.add(history_2)
        db.session.commit()

        service = PackageTimelineService()

        timeline = service.get_timeline(package.id)

        assert len(timeline) == 2

        assert timeline[0].status == "PROCESSING"
        assert timeline[1].status == "DISPATCHED"

        assert timeline[0].created_at == time_1
        assert timeline[1].created_at == time_2


def test_get_timeline_empty(app):
    with app.app_context():
        package = create_test_package()

        service = PackageTimelineService()

        timeline = service.get_timeline(package.id)

        assert timeline == []


def test_get_timeline_package_not_found(app):
    with app.app_context():
        service = PackageTimelineService()

        with pytest.raises(PackageNotFoundError):
            service.get_timeline(999)