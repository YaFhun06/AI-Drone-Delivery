from flask import Blueprint, jsonify

from src.services.notification_service import NotificationService

notification_bp = Blueprint("notification", __name__)
notification_service = NotificationService()


@notification_bp.route("/api/notifications/customer/<int:customer_id>", methods=["GET"])
def get_customer_notifications(customer_id):
    notifications = notification_service.get_customer_notifications(customer_id)
    return jsonify([n.to_dict() for n in notifications]), 200


@notification_bp.route("/api/notifications/<int:notification_id>/read", methods=["PUT"])
def mark_notification_read(notification_id):
    notification = notification_service.mark_as_read(notification_id)
    if not notification:
        return jsonify({"error": "Không tìm thấy thông báo"}), 404
    return jsonify(notification.to_dict()), 200