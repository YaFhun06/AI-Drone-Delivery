from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.services.auth_service import AuthService
from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.exceptions import DomainException

from flask_jwt_extended import jwt_required, get_jwt_identity

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

@auth_bp.route("/api/auth/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email là bắt buộc"}), 400

    try:
        auth_service.forgot_password(email)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({"message": "Mã xác nhận đã được gửi (kiểm tra console server)"}), 200


@auth_bp.route("/api/auth/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Mã xác nhận và mật khẩu mới là bắt buộc"}), 400

    try:
        auth_service.reset_password(token, new_password)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({"message": "Đặt lại mật khẩu thành công"}), 200

@auth_bp.route("/api/users/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()

    try:
        user = auth_service.get_profile(user_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "role_id": user.role_id,
    }), 200


@auth_bp.route("/api/users/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        user = auth_service.update_profile(
            user_id,
            full_name=data.get("full_name"),
            phone=data.get("phone"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({"message": "Cập nhật hồ sơ thành công", "full_name": user.full_name, "phone": user.phone}), 200