from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/test-login', methods=['POST'])
def test_login():
    data = request.get_json()
    email = data.get('email', 'test@example.com')
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/api/auth/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message=f"Xin chào {current_user}, bạn đã xác thực thành công!"), 200