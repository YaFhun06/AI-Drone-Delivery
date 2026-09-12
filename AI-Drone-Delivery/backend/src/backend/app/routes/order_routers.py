from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.order import Order
from app.models.station import Station  # Hoặc đường dẫn import Station thực tế trong dự án

order_bp = Blueprint('order', __name__, url_prefix='/api/orders')
@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """API Hủy đơn hàng (CNPM-83)"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.status = 'CANCELLED'
    db.session.commit()

    return jsonify({
        'message': 'Order cancelled successfully',
        'order': order.to_dict() if hasattr(order, 'to_dict') else {'id': order.id, 'status': order.status}
    }), 200


@order_bp.route('/<int:order_id>/auto-assign-station', methods=['POST'])
def auto_assign_station(order_id):
    """API Phân công đơn tự động cho trạm (CNPM-83)"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Tìm trạm (station) khả dụng đầu tiên hoặc trạm mặc định
    station = Station.query.first()
    if not station:
        return jsonify({'error': 'No available station found'}), 400

    order.station_id = station.id
    order.status = 'ASSIGNED'
    db.session.commit()

    return jsonify({
        'message': 'Station assigned successfully',
        'station_id': station.id,
        'order': order.to_dict() if hasattr(order, 'to_dict') else {'id': order.id, 'status': order.status}
    }), 200