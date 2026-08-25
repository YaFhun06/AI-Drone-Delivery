from src.infrastructure.repositories.address_repository import AddressRepository
from src.domain.exceptions import AddressNotFoundError

class AddressService:
    def __init__(self, address_repository: AddressRepository = None):
        self.address_repository = address_repository or AddressRepository()

    def get_all(self):
        return self.address_repository.find_all()

    def create(self, street, city, latitude, longitude):
        if not street:
            raise ValueError("street là bắt buộc")
        return self.address_repository.create(street, city, latitude, longitude)

    def get_by_id(self, address_id):
        address = self.address_repository.find_by_id(address_id)
        if not address:
            raise AddressNotFoundError()
        return address

    def update(self, address_id, street=None, city=None, latitude=None, longitude=None):
        address = self.get_by_id(address_id)
        return self.address_repository.update(address, street, city, latitude, longitude)

    def delete(self, address_id):
        address = self.get_by_id(address_id)
        self.address_repository.delete(address)