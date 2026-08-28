from flask import Blueprint, jsonify, request
from src.services.delivery_summary_service import DeliverySummaryService

delivery_summary_bp = Blueprint("delivery_summary", __name__)
delivery_summary_service = DeliverySummaryService()


@delivery_summary_bp.route("/api/deliveries/summarize", methods=["POST"])
def summarize_delivery():
    data = request.get_json()
    order_id = data.get("order_id")
    status_history = data.get("status_history")

    if not order_id or not status_history:
        return jsonify({"error": "Cần có order_id và status_history"}), 400

    try:
        summary = delivery_summary_service.summarize(order_id, status_history)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"order_id": order_id, "summary": summary}), 200