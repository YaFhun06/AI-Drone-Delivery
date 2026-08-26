from src.infrastructure.repositories.station_repository import StationRepository
from src.domain.exceptions import StationNotFoundError, InvalidStationStatusError
from src.domain.constants import StationStatus


class StationService:
    def __init__(self, station_repository: StationRepository = None):
        self.station_repository = station_repository or StationRepository()

    def list_stations(self):
        return self.station_repository.get_all()

    def get_station(self, station_id):
        station = self.station_repository.find_by_id(station_id)
        if not station:
            raise StationNotFoundError()
        return station

    def create_station(self, name, latitude, longitude, capacity, status):
        if status not in (StationStatus.ACTIVE, StationStatus.INACTIVE, StationStatus.MAINTENANCE):
            raise InvalidStationStatusError()
        return self.station_repository.create_station(name, latitude, longitude, capacity, status)

    def update_station(self, station_id, name=None, latitude=None, longitude=None, capacity=None, status=None):
        station = self.station_repository.find_by_id(station_id)
        if not station:
            raise StationNotFoundError()
        if status is not None and status not in (StationStatus.ACTIVE, StationStatus.INACTIVE, StationStatus.MAINTENANCE):
            raise InvalidStationStatusError()
        return self.station_repository.update_station(station, name=name, latitude=latitude, longitude=longitude, capacity=capacity, status=status)

    def update_status(self, station_id, status, latitude=None, longitude=None):
        if status not in (StationStatus.ACTIVE, StationStatus.INACTIVE, StationStatus.MAINTENANCE):
            raise InvalidStationStatusError()
        station = self.station_repository.find_by_id(station_id)
        if not station:
            raise StationNotFoundError()
        return self.station_repository.update_station(station, status=status, latitude=latitude, longitude=longitude)

    def delete_station(self, station_id):
        station = self.station_repository.find_by_id(station_id)
        if not station:
            raise StationNotFoundError()
        self.station_repository.delete_station(station)

    def get_capacity(self, station_id):
        station = self.station_repository.find_by_id(station_id)
        if not station:
            raise StationNotFoundError()
        active_orders_count = 0
        return {
            "station_id": station.id,
            "capacity": station.capacity,
            "active_orders": active_orders_count,
            "available": station.capacity - active_orders_count,
        }
