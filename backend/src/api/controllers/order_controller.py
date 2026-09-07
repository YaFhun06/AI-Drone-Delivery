from flask import Blueprint, request, jsonify
from src.services.order_service import OrderService
from src.domain.exceptions import DomainException

order_bp = Blueprint("order", __name__)
order_service = OrderService()


@order_bp.route("/api/orders/<int:order_id>/approve", methods=["PUT", "PATCH"])
def approve_order(order_id):
    try:
        order = order_service.approve_order(order_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code
    return jsonify({"message": "Order approved successfully", "status": order.status}), 200


@order_bp.route("/api/orders/<int:order_id>/reject", methods=["PUT", "PATCH"])
def reject_order(order_id):
    try:
        order = order_service.reject_order(order_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code
    return jsonify({"message": "Order rejected successfully", "status": order.status}), 200


@order_bp.route("/api/orders/<int:order_id>/schedule", methods=["POST", "PUT"])
def schedule_delivery(order_id):
    data = request.get_json()
    scheduled_time = data.get("scheduled_time")
    if not scheduled_time:
        return jsonify({"error": "Missing scheduled_time"}), 400

    try:
        order = order_service.schedule_delivery(
            order_id, scheduled_time, station_id=data.get("station_id")
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code
    return jsonify({"message": "Delivery scheduled successfully", "order": order.to_dict()}), 200
from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.databases.base import db

@order_bp.route("/api/orders", methods=["GET"])
def get_orders():
    try:
        orders = db.session.query(OrderModel).all()
        return jsonify([{
            "id": o.id,
            "customer_id": o.customer_id,
            "station_id": o.station_id,
            "status": o.status
        } for o in orders]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_bp.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order_detail(order_id):
    try:
        order = db.session.query(OrderModel).filter_by(id=order_id).first()
        if not order:
            return jsonify({"error": "Không tìm thấy đơn hàng"}), 404
        return jsonify({
            "id": order.id,
            "customer_id": order.customer_id,
            "station_id": order.station_id,
            "status": order.status
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500