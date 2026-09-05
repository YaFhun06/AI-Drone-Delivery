from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.drone import Drone

drone_bp = Blueprint('drone', __name__, url_prefix='/api/drones')

@drone_bp.route('', methods=['GET'])
def get_drones():
    drones = Drone.query.all()
    return jsonify([d.to_dict() for d in drones]), 200

@drone_bp.route('', methods=['POST'])
def create_drone():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400

    new_drone = Drone(
        name=data['name'],
        status=data.get('status', 'IDLE'),
        battery_level=data.get('battery_level', 100),
        station_id=data.get('station_id')
    )
    db.session.add(new_drone)
    db.session.commit()
    return jsonify(new_drone.to_dict()), 201

@drone_bp.route('/<int:drone_id>', methods=['GET'])
def get_drone(drone_id):
    drone = Drone.query.get_or_404(drone_id)
    return jsonify(drone.to_dict()), 200

@drone_bp.route('/<int:drone_id>', methods=['PUT'])
def update_drone(drone_id):
    drone = Drone.query.get_or_404(drone_id)
    data = request.get_json() or {}

    drone.name = data.get('name', drone.name)
    drone.status = data.get('status', drone.status)
    drone.battery_level = data.get('battery_level', drone.battery_level)
    drone.station_id = data.get('station_id', drone.station_id)

    db.session.commit()
    return jsonify(drone.to_dict()), 200

@drone_bp.route('/<int:drone_id>', methods=['DELETE'])
def delete_drone(drone_id):
    drone = Drone.query.get_or_404(drone_id)
    db.session.delete(drone)
    db.session.commit()
    return jsonify({'message': f'Drone {drone_id} deleted successfully'}), 200