from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.services.auth_service import AuthService
from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.exceptions import DomainException

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService(UserRepository())


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not email or not password:
        return jsonify({"error": "Email và mật khẩu là bắt buộc"}), 400

    try:
        user = auth_service.register(email, password, full_name)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({"message": "Đăng ký thành công", "user_id": user.id}), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email và mật khẩu là bắt buộc"}), 400

    try:
        result = auth_service.login(email, password)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    user = result["user"]
    return jsonify({
        "message": "Đăng nhập thành công",
        "access_token": result["access_token"],
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role_id": user.role_id,
        },
    }), 200


@auth_bp.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Đăng xuất thành công"}), 200