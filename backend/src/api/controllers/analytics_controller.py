from flask import Blueprint, jsonify
from src.services.analytics_service import AnalyticsService

analytics_bp = Blueprint("analytics", __name__)
analytics_service = AnalyticsService()


@analytics_bp.route("/api/analytics/orders-by-status", methods=["GET"])
def get_orders_by_status():
    summary = analytics_service.get_order_status_summary()
    return jsonify(summary), 200
@analytics_bp.route("/api/analytics/station-performance", methods=["GET"])
def get_station_performance():
    data = analytics_service.get_station_performance()
    return jsonify(data), 200

@analytics_bp.route("/api/analytics/success-rate", methods=["GET"])
def get_success_rate():
    data = analytics_service.get_delivery_success_rate()
    return jsonify(data), 200

@analytics_bp.route("/api/analytics/operating-cost", methods=["GET"])
def get_operating_cost():
    data = analytics_service.get_operating_cost_summary()
    return jsonify(data), 200