from src.infrastructure.repositories.customer_repository import CustomerRepository
from src.domain.exceptions import CustomerNotFoundError

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository = None):
        self.customer_repository = customer_repository or CustomerRepository()

    def get_by_id(self, customer_id):
        customer = self.customer_repository.find_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError()
        return customer

    def update(self, customer_id, full_name=None, phone=None, address_id=None):
        customer = self.get_by_id(customer_id)
        return self.customer_repository.update(customer, full_name, phone, address_id)