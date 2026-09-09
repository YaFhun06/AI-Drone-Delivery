from src.infrastructure.repositories.notification_repository import NotificationRepository
from src.sockets import emit_notification


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository = None):
        self.notification_repository = notification_repository or NotificationRepository()

    def notify_order_status(self, customer_id, order_id, status):
        messages = {
            "APPROVED": f"Don hang #{order_id} cua ban da duoc duyet.",
            "REJECTED": f"Don hang #{order_id} cua ban da bi tu choi.",
            "COMPLETED": f"Don hang #{order_id} da giao thanh cong.",
            "FAILED": f"Don hang #{order_id} giao hang that bai.",
            "SCHEDULED": f"Don hang #{order_id} da duoc len lich giao hang.",
        }
        message = messages.get(status, f"Don hang #{order_id} cap nhat trang thai: {status}")
        notification = self.notification_repository.create(
            customer_id=customer_id, order_id=order_id,
            message=message, type=status,
        )

        # Bắn realtime tới client đang lắng nghe của customer này
        emit_notification(customer_id, notification.to_dict())

        return notification

    def get_customer_notifications(self, customer_id):
        return self.notification_repository.find_by_customer(customer_id)

    def mark_as_read(self, notification_id):
        notification = self.notification_repository.find_by_id(notification_id)
        if notification:
            return self.notification_repository.mark_as_read(notification)
        return None