from src.infrastructure.repositories.order_repository import OrderRepository
from src.domain.exceptions import OrderNotFoundError


class OrderService:
    def __init__(self, order_repository: OrderRepository = None):
        self.order_repository = order_repository or OrderRepository()

    def approve_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()
        return self.order_repository.update_status(order, "APPROVED")

    def reject_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()
        return self.order_repository.update_status(order, "REJECTED")

    def schedule_delivery(self, order_id, scheduled_time, station_id=None):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()
        return self.order_repository.set_delivery_schedule(order, scheduled_time, station_id)