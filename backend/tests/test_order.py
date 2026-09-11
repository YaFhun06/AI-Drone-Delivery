from src.infrastructure.databases.base import db
from src.infrastructure.models.order_model import OrderModel
from src.services.order_service import OrderService


def create_test_order(app):
    with app.app_context():
        order = OrderModel(
            customer_id=1,
            status="APPROVED",
            retry_count=0
        )

        db.session.add(order)
        db.session.commit()

        return order.id


def test_fail_order(app):
    order_id = create_test_order(app)

    with app.app_context():
        service = OrderService()

        order = service.fail_order(
            order_id,
            "Drone gặp sự cố kỹ thuật"
        )

        assert order.status == "FAILED"
        assert order.failure_reason == "Drone gặp sự cố kỹ thuật"


def test_retry_order(app):
    order_id = create_test_order(app)

    with app.app_context():
        service = OrderService()

        service.fail_order(
            order_id,
            "Drone gặp sự cố kỹ thuật"
        )

        order = service.retry_order(order_id)

        assert order.status == "APPROVED"
        assert order.retry_count == 1
        assert order.failure_reason is None


def test_retry_non_failed_order(app):
    order_id = create_test_order(app)

    with app.app_context():
        service = OrderService()

        try:
            service.retry_order(order_id)
            assert False
        except ValueError as e:
            assert str(e) == "Only failed orders can be retried"


def test_fail_order_without_reason(app):
    order_id = create_test_order(app)

    with app.app_context():
        service = OrderService()

        try:
            service.fail_order(order_id, None)
            assert False
        except ValueError as e:
            assert str(e) == "Failure reason is required"