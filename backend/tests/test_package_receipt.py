from src.infrastructure.databases.base import db
from src.infrastructure.models.station_model import StationModel
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.role_model import RoleModel


class TestPackageReceiptEndpoints:

    def create_test_user(self):
        role = RoleModel.query.filter_by(name="Operator").first()

        if not role:
            role = RoleModel(
                name="Operator",
                description="Test Operator"
            )
            db.session.add(role)
            db.session.commit()

        user = UserModel(
            full_name="Test Operator",
            email="operator@test.com",
            password_hash="test_password",
            role_id=role.id
        )

        db.session.add(user)
        db.session.commit()

        return user

    def create_test_station(self):
        station = StationModel(
            name="Test Station",
            capacity=100,
            latitude=10.762622,
            longitude=106.660172,
            status="ACTIVE"
        )

        db.session.add(station)
        db.session.commit()

        return station

    def test_create_package_receipt(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            self.create_test_user()
            station = self.create_test_station()
            station_id = station.id

        response = client.post(
            "/api/package-receipts",
            json={
                "package_id": 1,
                "station_id": station_id
            },
            headers=auth_headers
        )

        assert response.status_code == 201

        data = response.get_json()

        assert data["package_id"] == 1
        assert data["station_id"] == station_id
        assert "id" in data
        assert "received_at" in data

    def test_create_receipt_station_not_found(
        self,
        client,
        auth_headers
    ):
        response = client.post(
            "/api/package-receipts",
            json={
                "package_id": 1,
                "station_id": 99999
            },
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_create_duplicate_package_receipt(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            self.create_test_user()
            station = self.create_test_station()
            station_id = station.id

        first_response = client.post(
            "/api/package-receipts",
            json={
                "package_id": 1,
                "station_id": station_id
            },
            headers=auth_headers
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/api/package-receipts",
            json={
                "package_id": 1,
                "station_id": station_id
            },
            headers=auth_headers
        )

        assert second_response.status_code == 400

    def test_list_package_receipts(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            self.create_test_user()
            station = self.create_test_station()
            station_id = station.id

        client.post(
            "/api/package-receipts",
            json={
                "package_id": 1,
                "station_id": station_id
            },
            headers=auth_headers
        )

        response = client.get(
            "/api/package-receipts"
        )

        assert response.status_code == 200

        data = response.get_json()

        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_package_receipt(
        self,
        app,
        client,
        auth_headers
    ):
        with app.app_context():
            self.create_test_user()
            station = self.create_test_station()
            station_id = station.id

        create_response = client.post(
            "/api/package-receipts",
            json={
                "package_id": 1,
                "station_id": station_id
            },
            headers=auth_headers
        )

        assert create_response.status_code == 201

        receipt_id = create_response.get_json()["id"]

        response = client.get(
            f"/api/package-receipts/{receipt_id}"
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["id"] == receipt_id
        assert data["package_id"] == 1
        assert data["station_id"] == station_id

    def test_get_package_receipt_not_found(
        self,
        client
    ):
        response = client.get(
            "/api/package-receipts/99999"
        )

        assert response.status_code == 404