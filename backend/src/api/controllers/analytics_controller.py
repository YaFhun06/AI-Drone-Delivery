from flask import Blueprint, jsonify, request
from src.services.analytics_service import AnalyticsService

analytics_bp = Blueprint("analytics", __name__)
analytics_service = AnalyticsService()


@analytics_bp.route("/api/analytics/orders-by-status", methods=["GET"])
def get_orders_by_status():
    return jsonify(analytics_service.get_order_status_summary()), 200


@analytics_bp.route("/api/analytics/operating-cost", methods=["GET"])
def get_operating_cost():
    return jsonify(analytics_service.get_operating_cost_summary()), 200


@analytics_bp.route("/api/analytics/station-performance", methods=["GET"])
def get_station_performance():
    return jsonify(analytics_service.get_station_performance()), 200


@analytics_bp.route("/api/analytics/success-rate", methods=["GET"])
def get_success_rate():
    return jsonify(analytics_service.get_delivery_success_rate()), 200

@analytics_bp.route("/api/analytics/orders-trend", methods=["GET"])
def get_orders_trend():
    days = request.args.get("days", default=7, type=int)
    return jsonify(analytics_service.get_orders_trend(days)), 200
