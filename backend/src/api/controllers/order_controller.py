from flask import Blueprint, request, jsonify
from src.services.order_service import OrderService
from src.domain.exceptions import DomainException
from src.api.decorators import require_permission

order_bp = Blueprint("order", __name__)
order_service = OrderService()


@order_bp.route("/api/orders/<int:order_id>/approve", methods=["PUT", "PATCH"])
@require_permission("approve_order")
def approve_order(order_id):
    try:
        order = order_service.approve_order(order_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code
    return jsonify({"message": "Order approved successfully", "status": order.status}), 200


@order_bp.route("/api/orders/<int:order_id>/reject", methods=["PUT", "PATCH"])
@require_permission("reject_order")
def reject_order(order_id):
    try:
        order = order_service.reject_order(order_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code
    return jsonify({"message": "Order rejected successfully", "status": order.status}), 200


@order_bp.route("/api/orders/<int:order_id>/schedule", methods=["POST", "PUT"])
@require_permission("schedule_delivery")
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