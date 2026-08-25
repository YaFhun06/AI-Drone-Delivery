from flask import Blueprint, jsonify, request
from src.services.address_service import AddressService
from src.infrastructure.repositories.address_repository import AddressRepository
from src.domain.exceptions import DomainException

address_bp = Blueprint("address", __name__)
address_service = AddressService(AddressRepository())


@address_bp.route("/api/addresses", methods=["POST"])
def create_address():
    data = request.get_json()
    try:
        address = address_service.create(
            street=data.get("street"),
            city=data.get("city"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "id": address.id, "street": address.street, "city": address.city,
        "latitude": address.latitude, "longitude": address.longitude
    }), 201


@address_bp.route("/api/addresses", methods=["GET"])
def get_addresses():
    addresses = address_service.get_all()
    return jsonify([{
        "id": a.id, "street": a.street, "city": a.city,
        "latitude": a.latitude, "longitude": a.longitude
    } for a in addresses]), 200


@address_bp.route("/api/addresses/<int:id>", methods=["PUT"])
def update_address(id):
    data = request.get_json()
    try:
        address = address_service.update(
            id,
            street=data.get("street"),
            city=data.get("city"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": address.id, "street": address.street, "city": address.city,
        "latitude": address.latitude, "longitude": address.longitude
    }), 200


@address_bp.route("/api/addresses/<int:id>", methods=["DELETE"])
def delete_address(id):
    try:
        address_service.delete(id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({"message": "Xóa địa chỉ thành công"}), 200