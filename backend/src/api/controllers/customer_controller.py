from flask import Blueprint, jsonify, request
from src.services.customer_service import CustomerService
from src.infrastructure.repositories.customer_repository import CustomerRepository
from src.domain.exceptions import DomainException

customer_bp = Blueprint("customer", __name__)
customer_service = CustomerService(CustomerRepository())


@customer_bp.route("/api/customers/<int:id>", methods=["GET"])
def get_customer(id):
    try:
        customer = customer_service.get_by_id(id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": customer.id, "full_name": customer.full_name,
        "phone": customer.phone, "address_id": customer.address_id
    }), 200
@customer_bp.route("/api/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    data = request.get_json()
    try:
        customer = customer_service.update(
            id,
            full_name=data.get("full_name"),
            phone=data.get("phone"),
            address_id=data.get("address_id"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": customer.id, "full_name": customer.full_name, "phone": customer.phone
    }), 200
