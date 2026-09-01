from app import db
from app.models.order import Order

class OrderRepository:
    @staticmethod
    def get_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def update_status(order, new_status):
        order.status = new_status
        db.session.commit()
        return order

    @staticmethod
    def set_delivery_schedule(order, scheduled_time):
        order.scheduled_delivery_time = scheduled_time
        order.status = 'SCHEDULED'
        db.session.commit()
        return order