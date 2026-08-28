from flask import Blueprint, jsonify, request
from src.services.eta_service import ETAService

eta_bp = Blueprint("eta", __name__)
eta_service = ETAService()


@eta_bp.route("/api/eta/estimate", methods=["POST"])
def estimate_eta():
    data = request.get_json()

    required = ["origin_lat", "origin_lng", "dest_lat", "dest_lng"]
    missing = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({"error": f"Thiếu trường bắt buộc: {', '.join(missing)}"}), 400

    result = eta_service.estimate(
        origin_lat=data["origin_lat"],
        origin_lng=data["origin_lng"],
        dest_lat=data["dest_lat"],
        dest_lng=data["dest_lng"],
        speed_kmh=data.get("speed_kmh"),
    )
    return jsonify(result), 200