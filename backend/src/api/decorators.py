from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.auth_function_model import AuthFunctionModel
from src.infrastructure.models.auth_role_function_model import AuthRoleFunctionModel


def require_permission(function_name):
    """
    Decorator kiểm tra role của user hiện tại có được gán quyền
    truy cập function_name (khớp với AuthFunctionModel.name) hay không.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = UserModel.query.get(user_id)

            if not user:
                return jsonify({"error": "Không tìm thấy người dùng"}), 401

            function = AuthFunctionModel.query.filter_by(name=function_name).first()
            if not function:
                # Chức năng chưa được khai báo trong hệ thống -> mặc định chặn để an toàn
                return jsonify({"error": "Chức năng chưa được cấu hình quyền"}), 403

            has_permission = AuthRoleFunctionModel.query.filter_by(
                role_id=user.role_id, function_id=function.id
            ).first()

            if not has_permission:
                return jsonify({"error": "Bạn không có quyền thực hiện thao tác này"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator