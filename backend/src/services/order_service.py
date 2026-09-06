from src.infrastructure.repositories.order_repository import OrderRepository
from src.domain.exceptions import OrderNotFoundError
from src.services.notification_service import NotificationService


class OrderService:
    def __init__(self, order_repository: OrderRepository = None, notification_service: NotificationService = None):
        self.order_repository = order_repository or OrderRepository()
        self.notification_service = notification_service or NotificationService()

    def approve_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()
        updated = self.order_repository.update_status(order, "APPROVED")
        self.notification_service.notify_order_status(order.customer_id, order.id, "APPROVED")
        return updated

    def reject_order(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()
        updated = self.order_repository.update_status(order, "REJECTED")
        self.notification_service.notify_order_status(order.customer_id, order.id, "REJECTED")
        return updated

    def schedule_delivery(self, order_id, scheduled_time, station_id=None):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()
        updated = self.order_repository.set_delivery_schedule(order, scheduled_time, station_id)
        self.notification_service.notify_order_status(order.customer_id, order.id, "SCHEDULED")
        return updated