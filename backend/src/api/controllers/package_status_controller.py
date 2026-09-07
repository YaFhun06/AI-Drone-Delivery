from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.services.package_status_service import PackageStatusService
from src.domain.exceptions import DomainException


package_status_bp = Blueprint("package_status", __name__)
package_status_service = PackageStatusService()


@package_status_bp.route(
    "/api/packages/<int:package_id>/status",
    methods=["PUT"]
)
@jwt_required()
def update_package_status(package_id):
    data = request.get_json() or {}
    new_status = data.get("status")

    try:
        package = package_status_service.update_status(
            package_id=package_id,
            new_status=new_status
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": package.id,
        "order_id": package.order_id,
        "status": package.status,
        "message": "Cập nhật trạng thái package thành công",
    }), 200