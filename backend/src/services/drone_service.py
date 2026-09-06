from src.infrastructure.repositories.drone_repository import DroneRepository
from src.domain.exceptions import DroneNotFoundError


class DroneService:
    def __init__(self, drone_repository: DroneRepository = None):
        self.drone_repository = drone_repository or DroneRepository()

    def get_all(self):
        return self.drone_repository.find_all()

    def get_by_id(self, drone_id):
        drone = self.drone_repository.find_by_id(drone_id)
        if not drone:
            raise DroneNotFoundError()
        return drone

    def create(self, name, status='IDLE', battery_level=100, station_id=None):
        if not name:
            raise ValueError("Tên drone là bắt buộc")
        return self.drone_repository.create(name, status, battery_level, station_id)

    def update(self, drone_id, name=None, status=None, battery_level=None, station_id=None):
        drone = self.get_by_id(drone_id)
        return self.drone_repository.update(drone, name, status, battery_level, station_id)

    def delete(self, drone_id):
        drone = self.get_by_id(drone_id)
        self.drone_repository.delete(drone)

    def confirm_return(self, drone_id, status='RETURNING', battery_level=None):
        drone = self.get_by_id(drone_id)
        return self.drone_repository.update(drone, status=status, battery_level=battery_level)