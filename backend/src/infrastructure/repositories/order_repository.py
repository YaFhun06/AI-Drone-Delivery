from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.databases.base import db


class OrderRepository:
    def find_by_id(self, order_id):
        return OrderModel.query.get(order_id)

    def update_status(self, order, new_status):
        order.status = new_status
        db.session.commit()
        return order

    def set_delivery_schedule(self, order, scheduled_time, station_id=None):
        order.scheduled_time = scheduled_time
        if station_id is not None:
            order.station_id = station_id
        order.status = 'SCHEDULED'
        db.session.commit()
        return order

    def mark_failed(self, order, failure_reason):
        order.status = 'FAILED'
        order.failure_reason = failure_reason
        db.session.commit()
        return order

    def retry_order(self, order):
        order.status = 'APPROVED'
        order.retry_count += 1
        order.failure_reason = None
        db.session.commit()
        return order