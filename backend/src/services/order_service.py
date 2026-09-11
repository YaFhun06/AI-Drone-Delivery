from src.infrastructure.repositories.order_repository import OrderRepository
from src.domain.exceptions import OrderNotFoundError
from src.services.notification_service import NotificationService
from src.sockets import emit_order_update


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository = None,
        notification_service: NotificationService = None
    ):
        self.order_repository = order_repository or OrderRepository()
        self.notification_service = (
            notification_service or NotificationService()
        )

    def approve_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundError()

        updated = self.order_repository.update_status(
            order,
            "APPROVED"
        )

        self.notification_service.notify_order_status(
            order.customer_id,
            order.id,
            "APPROVED"
        )

        emit_order_update(
            updated.id,
            {
                "order_id": updated.id,
                "status": updated.status
            }
        )

        return updated

    def reject_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundError()

        updated = self.order_repository.update_status(
            order,
            "REJECTED"
        )

        self.notification_service.notify_order_status(
            order.customer_id,
            order.id,
            "REJECTED"
        )

        emit_order_update(
            updated.id,
            {
                "order_id": updated.id,
                "status": updated.status
            }
        )

        return updated

    def complete_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundError()

        updated = self.order_repository.update_status(
            order,
            "COMPLETED"
        )

        self.notification_service.notify_order_status(
            order.customer_id,
            order.id,
            "COMPLETED"
        )

        emit_order_update(
            updated.id,
            {
                "order_id": updated.id,
                "status": updated.status
            }
        )

        return updated

    def schedule_delivery(
        self,
        order_id,
        scheduled_time,
        station_id=None
    ):
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundError()

        updated = self.order_repository.set_delivery_schedule(
            order,
            scheduled_time,
            station_id
        )

        self.notification_service.notify_order_status(
            order.customer_id,
            order.id,
            "SCHEDULED"
        )

        emit_order_update(
            updated.id,
            {
                "order_id": updated.id,
                "status": updated.status
            }
        )

        return updated

    def fail_order(self, order_id, failure_reason):
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundError()

        if not failure_reason:
            raise ValueError("Failure reason is required")

        updated = self.order_repository.mark_failed(
            order,
            failure_reason
        )

        self.notification_service.notify_order_status(
            order.customer_id,
            order.id,
            "FAILED"
        )

        emit_order_update(
            updated.id,
            {
                "order_id": updated.id,
                "status": updated.status,
                "failure_reason": updated.failure_reason
            }
        )

        return updated

    def retry_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundError()

        if order.status != "FAILED":
            raise ValueError(
                "Only failed orders can be retried"
            )

        updated = self.order_repository.retry_order(order)

        self.notification_service.notify_order_status(
            order.customer_id,
            order.id,
            "APPROVED"
        )

        emit_order_update(
            updated.id,
            {
                "order_id": updated.id,
                "status": updated.status,
                "retry_count": updated.retry_count
            }
        )

        return updated

    def get_all(self):
        return self.order_repository.find_all()

    def get_by_id(self, order_id):
        order = self.order_repository.find_by_id(order_id)

        if not order:
            raise OrderNotFoundError()

        return order