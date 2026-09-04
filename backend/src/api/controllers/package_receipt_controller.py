from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.package_receipt_service import PackageReceiptService
from src.domain.exceptions import DomainException


package_receipt_bp = Blueprint("package_receipt", __name__)
package_receipt_service = PackageReceiptService()


@package_receipt_bp.route("/api/package-receipts", methods=["GET"])
def list_receipts():
    try:
        receipts = package_receipt_service.list_receipts()
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify([
        {
            "id": receipt.id,
            "package_id": receipt.package_id,
            "station_id": receipt.station_id,
            "received_at": receipt.received_at.isoformat(),
            "received_by": receipt.received_by,
        }
        for receipt in receipts
    ]), 200


@package_receipt_bp.route(
    "/api/package-receipts/<int:receipt_id>",
    methods=["GET"]
)
def get_receipt(receipt_id):
    try:
        receipt = package_receipt_service.get_receipt(receipt_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": receipt.id,
        "package_id": receipt.package_id,
        "station_id": receipt.station_id,
        "received_at": receipt.received_at.isoformat(),
        "received_by": receipt.received_by,
    }), 200


@package_receipt_bp.route("/api/package-receipts", methods=["POST"])
@jwt_required()
def create_receipt():
    data = request.get_json() or {}

    try:
        received_by = get_jwt_identity()

        receipt = package_receipt_service.create_receipt(
            package_id=data.get("package_id"),
            station_id=data.get("station_id"),
            received_by=received_by,
            received_at=data.get("received_at"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": receipt.id,
        "package_id": receipt.package_id,
        "station_id": receipt.station_id,
        "received_at": receipt.received_at.isoformat(),
        "received_by": receipt.received_by,
        "message": "Xác nhận package đến trạm thành công",
    }), 201