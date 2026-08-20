from flask import Blueprint, request, jsonify
from app import db
from app.models.address import Address

address_bp = Blueprint('address', __name__)

# 1. GET /api/addresses - Lấy danh sách địa chỉ
@address_bp.route('/api/addresses', methods=['GET'])
def get_addresses():
    try:
        addresses = Address.query.all()
        result = []
        for addr in addresses:
            data = {c.name: getattr(addr, c.name) for c in addr.__table__.columns}
            for key in ['latitude', 'longitude']:
                if key in data and data[key] is not None:
                    data[key] = float(data[key])
            result.append(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. POST /api/addresses - Tạo địa chỉ mới
@address_bp.route('/api/addresses', methods=['POST'])
def create_address():
    try:
        data = request.get_json() or {}
        valid_columns = [c.name for c in Address.__table__.columns if not c.primary_key]
        
        filtered_data = {}
        for col in valid_columns:
            if col in data:
                filtered_data[col] = data[col]
            elif col == 'street_address' and 'street' in data:
                filtered_data['street_address'] = data['street']

        new_address = Address(**filtered_data)
        db.session.add(new_address)
        db.session.commit()

        return jsonify({
            'message': 'Address created successfully',
            'id': new_address.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 3. PUT /api/addresses/<id> - Cập nhật địa chỉ theo ID
@address_bp.route('/api/addresses/<int:id>', methods=['PUT'])
def update_address(id):
    try:
        address = Address.query.get(id)
        if not address:
            return jsonify({'error': 'Address not found'}), 404

        data = request.get_json() or {}
        valid_columns = [c.name for c in Address.__table__.columns if not c.primary_key]

        for col in valid_columns:
            if col in data:
                setattr(address, col, data[col])
            elif col == 'street_address' and 'street' in data:
                setattr(address, 'street_address', data['street'])

        db.session.commit()
        return jsonify({'message': f'Address {id} updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 4. DELETE /api/addresses/<id> - Xóa địa chỉ theo ID
@address_bp.route('/api/addresses/<int:id>', methods=['DELETE'])
def delete_address(id):
    try:
        address = Address.query.get(id)
        if not address:
            return jsonify({'error': 'Address not found'}), 404

        db.session.delete(address)
        db.session.commit()
        return jsonify({'message': f'Address {id} deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500