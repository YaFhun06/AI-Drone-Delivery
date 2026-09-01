from flask import Blueprint, jsonify
from src.services.analytics_service import AnalyticsService

analytics_bp = Blueprint("analytics", __name__)
analytics_service = AnalyticsService()


@analytics_bp.route("/api/analytics/orders-by-status", methods=["GET"])
def get_orders_by_status():
    summary = analytics_service.get_order_status_summary()
    return jsonify(summary), 200