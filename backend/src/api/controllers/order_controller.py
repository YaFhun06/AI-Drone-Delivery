from flask import Blueprint, request, jsonify

from src.services.order_service import OrderService
from src.domain.exceptions import DomainException
from src.api.decorators import require_permission


order_bp = Blueprint("order", __name__)
order_service = OrderService()


# =========================================================
# GET ALL ORDERS
# =========================================================
@order_bp.route("/api/orders", methods=["GET"])
def get_orders():
    """
    Lấy danh sách tất cả đơn hàng.
    """
    try:
        orders = order_service.get_all()

        return jsonify(
            [order.to_dict() for order in orders]
        ), 200

    except DomainException as e:
        return jsonify({
            "error": e.message
        }), e.status_code

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# GET ORDER DETAIL
# =========================================================
@order_bp.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """
    Lấy thông tin chi tiết một đơn hàng.
    """
    try:
        order = order_service.get_by_id(order_id)

        return jsonify(
            order.to_dict()
        ), 200

    except DomainException as e:
        return jsonify({
            "error": e.message
        }), e.status_code

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# CREATE ORDER
# =========================================================
@order_bp.route("/api/orders", methods=["POST"])
def create_order():
    """
    Tạo một đơn hàng mới.
    """
    data = request.get_json() or {}

    customer_id = data.get("customer_id")
    station_id = data.get("station_id")

    if not customer_id:
        return jsonify({
            "error": "Missing customer_id"
        }), 400

    try:
        order = order_service.create_order(
            customer_id=customer_id,
            station_id=station_id
        )

        return jsonify(
            order.to_dict()
        ), 201

    except DomainException as e:
        return jsonify({
            "error": e.message
        }), e.status_code

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# APPROVE ORDER
# =========================================================
@order_bp.route(
    "/api/orders/<int:order_id>/approve",
    methods=["PUT", "PATCH"]
)
@require_permission("approve_order")
def approve_order(order_id):
    """
    Duyệt đơn hàng.
    """
    try:
        order = order_service.approve_order(order_id)

        return jsonify({
            "message": "Order approved successfully",
            "status": order.status
        }), 200

    except DomainException as e:
        return jsonify({
            "error": e.message
        }), e.status_code

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# REJECT ORDER
# =========================================================
@order_bp.route(
    "/api/orders/<int:order_id>/reject",
    methods=["PUT", "PATCH"]
)
@require_permission("reject_order")
def reject_order(order_id):
    """
    Từ chối đơn hàng.
    """
    data = request.get_json() or {}

    reason = data.get("reason")

    try:
        order = order_service.reject_order(
            order_id=order_id,
            reason=reason
        )

        return jsonify({
            "message": "Order rejected successfully",
            "status": order.status
        }), 200

    except TypeError:
        # Dùng trường hợp service hiện tại chỉ nhận order_id
        try:
            order = order_service.reject_order(order_id)

            return jsonify({
                "message": "Order rejected successfully",
                "status": order.status
            }), 200

        except DomainException as e:
            return jsonify({
                "error": e.message
            }), e.status_code

    except DomainException as e:
        return jsonify({
            "error": e.message
        }), e.status_code

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# SCHEDULE DELIVERY
# =========================================================
@order_bp.route(
    "/api/orders/<int:order_id>/schedule",
    methods=["POST", "PUT"]
)
@require_permission("schedule_delivery")
def schedule_delivery(order_id):
    """
    Lên lịch giao hàng cho đơn hàng.
    """
    data = request.get_json() or {}

    scheduled_time = data.get("scheduled_time")
    station_id = data.get("station_id")

    if not scheduled_time:
        return jsonify({
            "error": "Missing scheduled_time"
        }), 400

    try:
        order = order_service.schedule_delivery(
            order_id=order_id,
            scheduled_time=scheduled_time,
            station_id=station_id
        )

        return jsonify({
            "message": "Delivery scheduled successfully",
            "order": order.to_dict()
        }), 200

    except DomainException as e:
        return jsonify({
            "error": e.message
        }), e.status_code

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500