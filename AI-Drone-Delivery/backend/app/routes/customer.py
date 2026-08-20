from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

# Đảm bảo tên biến chính xác là customer_bp
customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/api/customers/<int:id>', methods=['GET'])
def get_customer_info(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'Customer not found'}), 404

        user_data = {c.name: getattr(user, c.name) for c in user.__table__.columns if c.name != 'password_hash'}
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/api/customers/<int:id>', methods=['PUT'])
def update_customer_info(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'Customer not found'}), 404

        data = request.get_json() or {}
        valid_columns = [c.name for c in User.__table__.columns if not c.primary_key and c.name != 'password_hash']

        for col in valid_columns:
            if col in data:
                setattr(user, col, data[col])

        db.session.commit()
        return jsonify({'message': f'Customer {id} info updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500