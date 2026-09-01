from app import db
from app.models.order import Order

class OrderRepository:
    @staticmethod
    def get_all():
        return Order.query.all()

    @staticmethod
    def get_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def create(order):
        db.session.add(order)
        db.session.commit()
        return order