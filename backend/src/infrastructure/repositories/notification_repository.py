from src.infrastructure.models.notification_model import NotificationModel
from src.infrastructure.databases.base import db


class NotificationRepository:
    def create(self, customer_id, message, order_id=None, type='INFO'):
        notification = NotificationModel(
            customer_id=customer_id, order_id=order_id,
            message=message, type=type,
        )
        db.session.add(notification)
        db.session.commit()
        return notification

    def find_by_id(self, notification_id):
        return NotificationModel.query.get(notification_id)

    def find_by_customer(self, customer_id):
        return NotificationModel.query.filter_by(customer_id=customer_id).order_by(
            NotificationModel.created_at.desc()
        ).all()

    def mark_as_read(self, notification):
        notification.is_read = True
        db.session.commit()
        return notification
