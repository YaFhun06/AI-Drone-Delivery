from app.repositories.order_repositories import OrderRepository

class OrderService:
    @staticmethod
    def approve_order(order_id):
        order = OrderRepository.get_by_id(order_id)
        if not order:
            return None, "Order not found"
        updated_order = OrderRepository.update_status(order, "APPROVED")
        return updated_order, None

    @staticmethod
    def reject_order(order_id):
        order = OrderRepository.get_by_id(order_id)
        if not order:
            return None, "Order not found"
        updated_order = OrderRepository.update_status(order, "REJECTED")
        return updated_order, None

    @staticmethod
    def schedule_delivery(order_id, scheduled_time):
        order = OrderRepository.get_by_id(order_id)
        if not order:
            return None, "Order not found"
        updated_order = OrderRepository.set_delivery_schedule(order, scheduled_time)
        return updated_order, None