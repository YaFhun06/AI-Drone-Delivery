from flask import Blueprint, request, jsonify
from src.services.drone_service import DroneService
from src.domain.exceptions import DomainException

drone_bp = Blueprint('drone', __name__, url_prefix='/api/drones')
drone_service = DroneService()


@drone_bp.route('', methods=['GET'])
def get_drones():
    drones = drone_service.get_all()
    return jsonify([d.to_dict() for d in drones]), 200


@drone_bp.route('', methods=['POST'])
def create_drone():
    data = request.get_json() or {}
    try:
        drone = drone_service.create(
            name=data.get('name'),
            status=data.get('status', 'IDLE'),
            battery_level=data.get('battery_level', 100),
            station_id=data.get('station_id'),
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(drone.to_dict()), 201


@drone_bp.route('/<int:drone_id>', methods=['GET'])
def get_drone(drone_id):
    try:
        drone = drone_service.get_by_id(drone_id)
    except DomainException as e:
        return jsonify({'error': e.message}), e.status_code
    return jsonify(drone.to_dict()), 200


@drone_bp.route('/<int:drone_id>', methods=['PUT'])
def update_drone(drone_id):
    data = request.get_json() or {}
    try:
        drone = drone_service.update(
            drone_id,
            name=data.get('name'),
            status=data.get('status'),
            battery_level=data.get('battery_level'),
            station_id=data.get('station_id'),
        )
    except DomainException as e:
        return jsonify({'error': e.message}), e.status_code
    return jsonify(drone.to_dict()), 200


@drone_bp.route('/<int:drone_id>', methods=['DELETE'])
def delete_drone(drone_id):
    try:
        drone_service.delete(drone_id)
    except DomainException as e:
        return jsonify({'error': e.message}), e.status_code
    return jsonify({'message': f'Drone {drone_id} deleted successfully'}), 200


@drone_bp.route('/<int:drone_id>/confirm-return', methods=['POST'])
def confirm_drone_return(drone_id):
    data = request.get_json() or {}
    try:
        drone = drone_service.confirm_return(
            drone_id,
            status=data.get('status', 'RETURNING'),
            battery_level=data.get('battery_level'),
        )
    except DomainException as e:
        return jsonify({'error': e.message}), e.status_code
    return jsonify({'message': 'Drone status updated successfully', 'drone': drone.to_dict()}), 200