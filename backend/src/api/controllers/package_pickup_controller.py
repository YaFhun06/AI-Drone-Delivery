from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.package_pickup_service import PackagePickupService
from src.domain.exceptions import DomainException


package_pickup_bp = Blueprint("package_pickup", __name__)
package_pickup_service = PackagePickupService()


@package_pickup_bp.route("/api/package-pickups", methods=["GET"])
def list_pickups():
    try:
        pickups = package_pickup_service.list_pickups()
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify([
        {
            "id": pickup.id,
            "package_id": pickup.package_id,
            "station_id": pickup.station_id,
            "picked_up_at": pickup.picked_up_at.isoformat(),
            "picked_up_by": pickup.picked_up_by,
        }
        for pickup in pickups
    ]), 200


@package_pickup_bp.route(
    "/api/package-pickups/<int:pickup_id>",
    methods=["GET"]
)
def get_pickup(pickup_id):
    try:
        pickup = package_pickup_service.get_pickup(pickup_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": pickup.id,
        "package_id": pickup.package_id,
        "station_id": pickup.station_id,
        "picked_up_at": pickup.picked_up_at.isoformat(),
        "picked_up_by": pickup.picked_up_by,
    }), 200


@package_pickup_bp.route("/api/package-pickups", methods=["POST"])
@jwt_required()
def create_pickup():
    data = request.get_json() or {}

    try:
        picked_up_by = get_jwt_identity()

        pickup = package_pickup_service.create_pickup(
            package_id=data.get("package_id"),
            station_id=data.get("station_id"),
            picked_up_by=picked_up_by,
            picked_up_at=data.get("picked_up_at"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": pickup.id,
        "package_id": pickup.package_id,
        "station_id": pickup.station_id,
        "picked_up_at": pickup.picked_up_at.isoformat(),
        "picked_up_by": pickup.picked_up_by,
        "message": "Xác nhận pickup package thành công",
    }), 201