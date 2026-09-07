from src.infrastructure.databases.base import db
from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.station_model import StationModel
from src.infrastructure.models.customer_model import CustomerModel
from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.models.package_model import PackageModel


class TestPackageStatusEndpoints:

    def create_test_data(self):
        role = RoleModel(
            name="StationOperator",
            description="Test operator"
        )
        db.session.add(role)
        db.session.flush()

        user = UserModel(
            full_name="Test Operator",
            email="operator@test.com",
            password_hash="test",
            role_id=role.id
        )
        db.session.add(user)

        station = StationModel(
            name="Test Station",
            capacity=10,
            latitude=10.8231,
            longitude=106.6297,
            status="ACTIVE"
        )
        db.session.add(station)

        db.session.flush()

        customer = CustomerModel(
            full_name="Test Customer",
            phone="0900000000"
        )
        db.session.add(customer)

        db.session.flush()

        order = OrderModel(
            customer_id=customer.id,
            station_id=station.id,
            status="APPROVED"
        )
        db.session.add(order)

        db.session.flush()

        package = PackageModel(
            order_id=order.id,
            weight=1.5,
            status="RECEIVED"
        )
        db.session.add(package)

        db.session.commit()

        return package.id

    def test_update_package_status_to_processing(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            package_id = self.create_test_data()

        response = client.put(
            f"/api/packages/{package_id}/status",
            json={
                "status": "PROCESSING"
            },
            headers=auth_headers
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["id"] == package_id
        assert data["status"] == "PROCESSING"

    def test_update_package_status_to_dispatched(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            package_id = self.create_test_data()

        first_response = client.put(
            f"/api/packages/{package_id}/status",
            json={
                "status": "PROCESSING"
            },
            headers=auth_headers
        )

        assert first_response.status_code == 200

        response = client.put(
            f"/api/packages/{package_id}/status",
            json={
                "status": "DISPATCHED"
            },
            headers=auth_headers
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "DISPATCHED"

    def test_package_not_found(
        self,
        client,
        auth_headers
    ):
        response = client.put(
            "/api/packages/99999/status",
            json={
                "status": "PROCESSING"
            },
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_invalid_status(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            package_id = self.create_test_data()

        response = client.put(
            f"/api/packages/{package_id}/status",
            json={
                "status": "INVALID"
            },
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_invalid_status_transition(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            package_id = self.create_test_data()

        response = client.put(
            f"/api/packages/{package_id}/status",
            json={
                "status": "DISPATCHED"
            },
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_cannot_update_dispatched_package(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            package_id = self.create_test_data()

        client.put(
            f"/api/packages/{package_id}/status",
            json={
                "status": "PROCESSING"
            },
            headers=auth_headers
        )

        client.put(
            f"/api/packages/{package_id}/status",
            json={
                "status": "DISPATCHED"
            },
            headers=auth_headers
        )

        response = client.put(
            f"/api/packages/{package_id}/status",
            json={
                "status": "PROCESSING"
            },
            headers=auth_headers
        )

        assert response.status_code == 400