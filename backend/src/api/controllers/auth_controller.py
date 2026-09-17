from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from src.domain.exceptions import DomainException
from src.infrastructure.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService


auth_bp = Blueprint(
    "auth",
    __name__,
)

auth_service = AuthService(
    UserRepository()
)


def get_json_body():
    """
    Đọc JSON body an toàn.

    Nếu request không có JSON hoặc JSON không phải object,
    trả về dictionary rỗng.
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {}

    return data


def validate_password(password):
    """
    Kiểm tra mật khẩu cơ bản.
    Có thể nâng cấp thêm theo yêu cầu SRS sau.
    """
    return (
        isinstance(password, str)
        and len(password) >= 6
    )


@auth_bp.route(
    "/api/auth/register",
    methods=["POST"],
)
def register():
    data = get_json_body()

    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not email or not password:
        return jsonify({
            "error": "Email và mật khẩu là bắt buộc",
        }), 400

    if not validate_password(password):
        return jsonify({
            "error": "Mật khẩu phải có ít nhất 6 ký tự",
        }), 400

    try:
        user = auth_service.register(
            email=email.strip().lower(),
            password=password,
            full_name=full_name,
        )

    except DomainException as error:
        return jsonify({
            "error": error.message,
        }), error.status_code

    return jsonify({
        "message": "Đăng ký thành công",
        "user_id": user.id,
    }), 201


@auth_bp.route(
    "/api/auth/login",
    methods=["POST"],
)
def login():
    data = get_json_body()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email và mật khẩu là bắt buộc",
        }), 400

    try:
        result = auth_service.login(
            email=email.strip().lower(),
            password=password,
        )

    except DomainException as error:
        return jsonify({
            "error": error.message,
        }), error.status_code

    user = result["user"]

    return jsonify({
        "message": "Đăng nhập thành công",
        "access_token": result["access_token"],
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "role_id": user.role_id,
            "is_active": user.is_active,
        },
    }), 200


@auth_bp.route(
    "/api/auth/logout",
    methods=["POST"],
)
@jwt_required()
def logout():
    """
    Logout phía client.

    Frontend/mobile phải xóa access_token sau khi gọi API này.
    Cơ chế blacklist JWT có thể bổ sung ở bước bảo mật nâng cao.
    """
    return jsonify({
        "message": "Đăng xuất thành công",
    }), 200


@auth_bp.route(
    "/api/auth/forgot-password",
    methods=["POST"],
)
def forgot_password():
    data = get_json_body()
    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email là bắt buộc",
        }), 400

    try:
        auth_service.forgot_password(
            email=email.strip().lower()
        )

    except DomainException as error:
        return jsonify({
            "error": error.message,
        }), error.status_code

    return jsonify({
        "message": (
            "Mã xác nhận đã được tạo. "
            "Trong môi trường demo, kiểm tra console server."
        ),
    }), 200


@auth_bp.route(
    "/api/auth/reset-password",
    methods=["POST"],
)
def reset_password():
    data = get_json_body()

    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({
            "error": (
                "Mã xác nhận và mật khẩu mới "
                "là bắt buộc"
            ),
        }), 400

    if not validate_password(new_password):
        return jsonify({
            "error": (
                "Mật khẩu mới phải có ít nhất "
                "6 ký tự"
            ),
        }), 400

    try:
        auth_service.reset_password(
            token=token,
            new_password=new_password,
        )

    except DomainException as error:
        return jsonify({
            "error": error.message,
        }), error.status_code

    return jsonify({
        "message": "Đặt lại mật khẩu thành công",
    }), 200


@auth_bp.route(
    "/api/users/profile",
    methods=["GET"],
)
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()

    try:
        user = auth_service.get_profile(
            user_id=user_id
        )

    except DomainException as error:
        return jsonify({
            "error": error.message,
        }), error.status_code

    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "role_id": user.role_id,
        "is_active": user.is_active,
    }), 200


@auth_bp.route(
    "/api/users/profile",
    methods=["PUT"],
)
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = get_json_body()

    full_name = data.get("full_name")
    phone = data.get("phone")

    if full_name is not None and not isinstance(full_name, str):
        return jsonify({
            "error": "full_name phải là chuỗi",
        }), 400

    if phone is not None and not isinstance(phone, str):
        return jsonify({
            "error": "phone phải là chuỗi",
        }), 400

    try:
        user = auth_service.update_profile(
            user_id=user_id,
            full_name=full_name,
            phone=phone,
        )

    except DomainException as error:
        return jsonify({
            "error": error.message,
        }), error.status_code

    return jsonify({
        "message": "Cập nhật hồ sơ thành công",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "role_id": user.role_id,
        },
    }), 200