from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from src.infrastructure.databases.base import db
from src.infrastructure.models.customer_model import CustomerModel
from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.models.user_model import UserModel

management_bp = Blueprint("management", __name__)


@management_bp.route("/api/users", methods=["GET"])
@jwt_required()
def list_users():
    rows = db.session.query(UserModel, RoleModel.name).outerjoin(
        RoleModel, UserModel.role_id == RoleModel.id
    ).order_by(UserModel.id.desc()).all()

    return jsonify([
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": role_name or "Chưa phân quyền",
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
        for user, role_name in rows
    ]), 200


@management_bp.route("/api/orders", methods=["GET"])
@jwt_required()
def list_orders():
    rows = db.session.query(OrderModel, CustomerModel.full_name).outerjoin(
        CustomerModel, OrderModel.customer_id == CustomerModel.id
    ).order_by(OrderModel.created_at.desc()).all()

    return jsonify([
        {
            **order.to_dict(),
            "customer_name": customer_name or "Chưa có khách hàng",
        }
        for order, customer_name in rows
    ]), 200
