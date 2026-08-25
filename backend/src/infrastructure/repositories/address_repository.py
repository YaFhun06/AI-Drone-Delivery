from src.infrastructure.models.address_model import AddressModel
from src.infrastructure.databases.base import db

class AddressRepository:
    def find_all(self):
        return AddressModel.query.all()

    def find_by_id(self, address_id):
        return AddressModel.query.get(address_id)

    def create(self, street, city, latitude, longitude):
        address = AddressModel(street=street, city=city, latitude=latitude, longitude=longitude)
        db.session.add(address)
        db.session.commit()
        return address

    def update(self, address, street=None, city=None, latitude=None, longitude=None):
        if street is not None:
            address.street = street
        if city is not None:
            address.city = city
        if latitude is not None:
            address.latitude = latitude
        if longitude is not None:
            address.longitude = longitude
        db.session.commit()
        return address

    def delete(self, address):
        db.session.delete(address)
        db.session.commit()