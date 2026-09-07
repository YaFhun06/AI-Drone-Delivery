from src.infrastructure.databases.base import db
from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.customer_model import CustomerModel
from src.infrastructure.models.order_model import OrderModel


class TestOrderTrackingEndpoints:

    def create_order(self):
        role = RoleModel(
            name="Customer"
        )

        db.session.add(role)
        db.session.commit()

        user = UserModel(
            full_name="Test User",
            email="test@example.com",
            password_hash="test-password",
            role_id=role.id
        )

        db.session.add(user)
        db.session.commit()

        customer = CustomerModel(
            user_id=user.id,
            full_name="Test Customer",
            phone="0123456789"
        )

        db.session.add(customer)
        db.session.commit()

        order = OrderModel(
            customer_id=customer.id,
            status="APPROVED"
        )

        db.session.add(order)
        db.session.commit()

        return order

    def test_complete_order(self, client, app):
        with app.app_context():
            order = self.create_order()
            order_id = order.id

        response = client.put(
            f"/api/orders/{order_id}/complete"
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "COMPLETED"

    def test_complete_order_not_found(self, client):
        response = client.put(
            "/api/orders/99999/complete"
        )

        assert response.status_code == 404

    def test_fail_order(self, client, app):
        with app.app_context():
            order = self.create_order()
            order_id = order.id

        response = client.put(
            f"/api/orders/{order_id}/fail",
            json={
                "failure_reason": "Drone battery failure"
            }
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "FAILED"
        assert data["failure_reason"] == "Drone battery failure"

    def test_fail_order_without_reason(self, client, app):
        with app.app_context():
            order = self.create_order()
            order_id = order.id

        response = client.put(
            f"/api/orders/{order_id}/fail",
            json={}
        )

        assert response.status_code == 400

    def test_retry_failed_order(self, client, app):
        with app.app_context():
            order = self.create_order()

            order.status = "FAILED"
            order.failure_reason = "Drone battery failure"

            db.session.commit()

            order_id = order.id

        response = client.put(
            f"/api/orders/{order_id}/retry"
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "APPROVED"
        assert data["retry_count"] == 1

    def test_retry_non_failed_order(self, client, app):
        with app.app_context():
            order = self.create_order()
            order_id = order.id

        response = client.put(
            f"/api/orders/{order_id}/retry"
        )

        assert response.status_code == 400