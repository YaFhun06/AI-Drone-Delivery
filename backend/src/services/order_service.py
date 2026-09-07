from src.sockets import emit_order_update
from src.infrastructure.repositories.order_repository import OrderRepository
from src.domain.exceptions import OrderNotFoundError


class OrderService:
    def __init__(self, order_repository: OrderRepository = None):
        self.order_repository = order_repository or OrderRepository()

    def _emit_status_update(self, order):
        emit_order_update(
            order.id,
            {
                "order_id": order.id,
                "status": order.status,
                "retry_count": order.retry_count
            }
        )

    def approve_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()

        updated = self.order_repository.update_status(order, "APPROVED")
        self._emit_status_update(updated)
        return updated

    def reject_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()

        updated = self.order_repository.update_status(order, "REJECTED")
        self._emit_status_update(updated)
        return updated

    def complete_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()

        updated = self.order_repository.update_status(order, "COMPLETED")
        self._emit_status_update(updated)
        return updated

    def schedule_delivery(self, order_id, scheduled_time, station_id=None):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()

        updated = self.order_repository.set_delivery_schedule(
            order, scheduled_time, station_id
        )
        self._emit_status_update(updated)
        return updated

    def fail_order(self, order_id, failure_reason):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()

        if not failure_reason:
            raise ValueError("Failure reason is required")

        updated = self.order_repository.mark_failed(order, failure_reason)
        self._emit_status_update(updated)
        return updated

    def retry_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()

        if order.status != "FAILED":
            raise ValueError("Only failed orders can be retried")

        updated = self.order_repository.retry_order(order)
        self._emit_status_update(updated)
        return updated