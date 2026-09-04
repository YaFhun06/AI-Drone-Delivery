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


@order_bp.route("/api/orders/<int:order_id>/complete", methods=["PUT", "PATCH"])
def complete_order(order_id):
    try:
        order = order_service.complete_order(order_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "message": "Order completed successfully",
        "status": order.status
    }), 200
@order_bp.route("/api/orders/<int:order_id>/fail", methods=["POST", "PUT", "PATCH"])
def fail_order(order_id):
    data = request.get_json() or {}
    failure_reason = data.get("failure_reason")

    if not failure_reason:
        return jsonify({"error": "Missing failure_reason"}), 400

    try:
        order = order_service.fail_order(order_id, failure_reason)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "message": "Order marked as failed",
        "status": order.status,
        "failure_reason": order.failure_reason,
        "retry_count": order.retry_count
    }), 200


@order_bp.route("/api/orders/<int:order_id>/retry", methods=["POST", "PUT", "PATCH"])
def retry_order(order_id):
    try:
        order = order_service.retry_order(order_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "message": "Order retry initiated successfully",
        "status": order.status,
        "retry_count": order.retry_count
    }), 200