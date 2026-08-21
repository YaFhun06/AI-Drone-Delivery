from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.services.role_service import RoleService

role_bp = Blueprint("role", __name__)
role_service = RoleService()

@role_bp.route("/api/roles", methods=["GET"])
@jwt_required()
def list_roles():
    roles = role_service.list_roles()
    return jsonify([{"id": r.id, "name": r.name, "description": r.description} for r in roles]), 200

@role_bp.route("/api/roles", methods=["POST"])
@jwt_required()
def create_role():
    data = request.get_json()
    role = role_service.create_role(data.get("name"), data.get("description"))
    return jsonify({"id": role.id, "name": role.name}), 201

@role_bp.route("/api/roles/<int:role_id>/functions", methods=["POST"])
@jwt_required()
def assign_function(role_id):
    data = request.get_json()
    function_id = data.get("function_id")
    role_service.assign_function_to_role(role_id, function_id)
    return jsonify({"message": "Gán quyền thành công"}), 201

@role_bp.route("/api/functions", methods=["GET"])
@jwt_required()
def list_functions():
    functions = role_service.list_functions()
    return jsonify([{"id": f.id, "name": f.name, "url": f.url} for f in functions]), 200