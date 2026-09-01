from app.repositories.order_repository import OrderRepository
from app.repositories.package_repository import PackageRepository
from app.models.order import Order
from app.models.package import Package

class OrderService:
    @staticmethod
    def get_all_orders():
        return OrderRepository.get_all()

    @staticmethod
    def get_order_by_id(order_id):
        return OrderRepository.get_by_id(order_id)

    @staticmethod
    def create_order_with_package(data):
        new_order = Order(
            customer_id=data.get('customer_id'),
            station_id=data.get('station_id'),
            scheduled_time=data.get('scheduled_time')
        )
        OrderRepository.create(new_order)

        if 'package' in data:
            pkg_data = data['package']
            new_package = Package(
                order_id=new_order.id,
                weight=pkg_data.get('weight'),
                dimensions=pkg_data.get('dimensions'),
                description=pkg_data.get('description')
            )
            PackageRepository.create(new_package)

        return new_order