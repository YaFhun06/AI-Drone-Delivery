from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = OrderService.get_all_orders()
    return jsonify([order.to_dict() for order in orders]), 200

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = OrderService.get_order_by_id(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    return jsonify(order.to_dict()), 200

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or not data.get('customer_id'):
        return jsonify({'message': 'Missing customer_id'}), 400

    new_order = OrderService.create_order_with_package(data)
    return jsonify(new_order.to_dict()), 201