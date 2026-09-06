from src.infrastructure.models.drone_model import DroneModel
from src.infrastructure.databases.base import db


class DroneRepository:
    def find_all(self):
        return DroneModel.query.all()

    def find_by_id(self, drone_id):
        return DroneModel.query.get(drone_id)

    def create(self, name, status='IDLE', battery_level=100, station_id=None):
        drone = DroneModel(name=name, status=status, battery_level=battery_level, station_id=station_id)
        db.session.add(drone)
        db.session.commit()
        return drone

    def update(self, drone, name=None, status=None, battery_level=None, station_id=None):
        if name is not None:
            drone.name = name
        if status is not None:
            drone.status = status
        if battery_level is not None:
            drone.battery_level = battery_level
        if station_id is not None:
            drone.station_id = station_id
        db.session.commit()
        return drone

    def delete(self, drone):
        db.session.delete(drone)
        db.session.commit()