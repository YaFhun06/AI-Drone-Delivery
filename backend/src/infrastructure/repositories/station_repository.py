from src.infrastructure.models.station_model import StationModel
from src.infrastructure.databases.base import db


class StationRepository:
    def get_all(self):
        return StationModel.query.all()

    def find_by_id(self, station_id):
        return StationModel.query.get(station_id)

    def create_station(self, name, latitude, longitude, capacity, status):
        station = StationModel(
            name=name,
            latitude=latitude,
            longitude=longitude,
            capacity=capacity,
            status=status,
        )
        db.session.add(station)
        db.session.commit()
        return station

    def update_station(self, station, name=None, latitude=None, longitude=None, capacity=None, status=None):
        if name is not None:
            station.name = name
        if latitude is not None:
            station.latitude = latitude
        if longitude is not None:
            station.longitude = longitude
        if capacity is not None:
            station.capacity = capacity
        if status is not None:
            station.status = status
        db.session.commit()
        return station

    def delete_station(self, station):
        db.session.delete(station)
        db.session.commit()
