from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService

# Giữ nguyên order_bp đã có
order_bp = Blueprint('order_bp', __name__)

# FR-12: Duyệt đơn
@order_bp.route('/orders/<int:order_id>/approve', methods=['PUT', 'PATCH'])
def approve_order(order_id):
    order, error = OrderService.approve_order(order_id)
    if error:
        return jsonify({'message': error}), 404
    return jsonify({'message': 'Order approved successfully', 'status': order.status}), 200

# FR-13: Từ chối đơn
@order_bp.route('/orders/<int:order_id>/reject', methods=['PUT', 'PATCH'])
def reject_order(order_id):
    order, error = OrderService.reject_order(order_id)
    if error:
        return jsonify({'message': error}), 404
    return jsonify({'message': 'Order rejected successfully', 'status': order.status}), 200

# FR-14: Lên lịch giao hàng
@order_bp.route('/orders/<int:order_id>/schedule', methods=['POST', 'PUT'])
def schedule_delivery(order_id):
    data = request.get_json()
    scheduled_time = data.get('scheduled_time')
    if not scheduled_time:
        return jsonify({'message': 'Missing scheduled_time'}), 400
        
    order, error = OrderService.schedule_delivery(order_id, scheduled_time)
    if error:
        return jsonify({'message': error}), 404
    return jsonify({'message': 'Delivery scheduled successfully', 'order': order.to_dict() if hasattr(order, 'to_dict') else {'id': order.id}}), 200