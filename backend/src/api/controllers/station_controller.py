from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.services.station_service import StationService
from src.domain.exceptions import DomainException

station_bp = Blueprint("station", __name__)
station_service = StationService()


@station_bp.route("/api/stations", methods=["GET"])
def list_stations():
    try:
        stations = station_service.list_stations()
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "capacity": s.capacity,
            "status": s.status,
        }
        for s in stations
    ]), 200


@station_bp.route("/api/stations/<int:station_id>", methods=["GET"])
def get_station(station_id):
    try:
        station = station_service.get_station(station_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": station.id,
        "name": station.name,
        "latitude": station.latitude,
        "longitude": station.longitude,
        "capacity": station.capacity,
        "status": station.status,
    }), 200


@station_bp.route("/api/stations", methods=["POST"])
@jwt_required()
def create_station():
    data = request.get_json()

    try:
        station = station_service.create_station(
            name=data.get("name"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            capacity=data.get("capacity"),
            status=data.get("status"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": station.id,
        "name": station.name,
        "latitude": station.latitude,
        "longitude": station.longitude,
        "capacity": station.capacity,
        "status": station.status,
    }), 201


@station_bp.route("/api/stations/<int:station_id>", methods=["PUT"])
@jwt_required()
def update_station(station_id):
    data = request.get_json()

    try:
        station = station_service.update_station(
            station_id,
            name=data.get("name"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            capacity=data.get("capacity"),
            status=data.get("status"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": station.id,
        "name": station.name,
        "latitude": station.latitude,
        "longitude": station.longitude,
        "capacity": station.capacity,
        "status": station.status,
    }), 200


@station_bp.route("/api/stations/<int:station_id>", methods=["DELETE"])
@jwt_required()
def delete_station(station_id):
    try:
        station_service.delete_station(station_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "message": "Xóa trạm thành công"
    }), 200
@station_bp.route("/api/stations/<int:station_id>/status", methods=["PUT"])
@jwt_required()
def update_station_status(station_id):
    data = request.get_json()

    try:
        station = station_service.update_status(
            station_id,
            status=data.get("status"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({
        "id": station.id,
        "name": station.name,
        "latitude": station.latitude,
        "longitude": station.longitude,
        "status": station.status,
    }), 200


@station_bp.route("/api/stations/<int:station_id>/capacity", methods=["GET"])
def get_station_capacity(station_id):
    try:
        result = station_service.get_capacity(station_id)
    except DomainException as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify(result), 200