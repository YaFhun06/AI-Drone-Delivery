from src.infrastructure.models.customer_model import CustomerModel
from src.infrastructure.databases.base import db

class CustomerRepository:
    def find_by_id(self, customer_id):
        return CustomerModel.query.get(customer_id)

    def update(self, customer, full_name=None, phone=None, address_id=None):
        if full_name is not None:
            customer.full_name = full_name
        if phone is not None:
            customer.phone = phone
        if address_id is not None:
            customer.address_id = address_id
        db.session.commit()
        return customer
    