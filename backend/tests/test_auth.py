import pytest
from src.infrastructure.databases.base import db
from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.models.user_model import UserModel
from werkzeug.security import generate_password_hash


@pytest.fixture
def customer_role(app):
    with app.app_context():
        role = RoleModel(name="Customer", description="Khách hàng")
        db.session.add(role)
        db.session.commit()
        return role.id


class TestAuthEndpoints:
    def test_register_success(self, client, customer_role):
        response = client.post(
            '/api/auth/register',
            json={
                'email': 'user1@example.com',
                'password': '123456',
                'full_name': 'Nguyen Van A',
            },
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'user_id' in data

    def test_register_missing_fields(self, client):
        response = client.post(
            '/api/auth/register',
            json={'email': '', 'password': ''},
        )
        assert response.status_code == 400

    def test_register_duplicate_email(self, client, customer_role):
        client.post(
            '/api/auth/register',
            json={'email': 'dup@example.com', 'password': '123456', 'full_name': 'A'},
        )
        response = client.post(
            '/api/auth/register',
            json={'email': 'dup@example.com', 'password': '123456', 'full_name': 'B'},
        )
        assert response.status_code == 400

    def test_register_role_not_configured(self, client):
        # Không seed Role Customer
        response = client.post(
            '/api/auth/register',
            json={'email': 'norole@example.com', 'password': '123456', 'full_name': 'A'},
        )
        assert response.status_code == 500

    def test_login_success(self, client, customer_role):
        client.post(
            '/api/auth/register',
            json={'email': 'login1@example.com', 'password': '123456', 'full_name': 'A'},
        )
        response = client.post(
            '/api/auth/login',
            json={'email': 'login1@example.com', 'password': '123456'},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert data['user']['email'] == 'login1@example.com'

    def test_login_wrong_password(self, client, customer_role):
        client.post(
            '/api/auth/register',
            json={'email': 'login2@example.com', 'password': '123456', 'full_name': 'A'},
        )
        response = client.post(
            '/api/auth/login',
            json={'email': 'login2@example.com', 'password': 'wrongpass'},
        )
        assert response.status_code == 401

    def test_login_missing_fields(self, client):
        response = client.post('/api/auth/login', json={'email': ''})
        assert response.status_code == 400

    def test_login_nonexistent_user(self, client):
        response = client.post(
            '/api/auth/login',
            json={'email': 'noone@example.com', 'password': '123456'},
        )
        assert response.status_code == 401

    def test_logout_requires_auth(self, client):
        response = client.post('/api/auth/logout')
        assert response.status_code == 401

    def test_logout_success(self, client, auth_headers):
        response = client.post('/api/auth/logout', headers=auth_headers)
        assert response.status_code == 200

    def test_forgot_password_success(self, client, customer_role):
        client.post(
            '/api/auth/register',
            json={'email': 'forgot1@example.com', 'password': '123456', 'full_name': 'A'},
        )
        response = client.post(
            '/api/auth/forgot-password',
            json={'email': 'forgot1@example.com'},
        )
        assert response.status_code == 200

    def test_forgot_password_missing_email(self, client):
        response = client.post('/api/auth/forgot-password', json={})
        assert response.status_code == 400

    def test_forgot_password_user_not_found(self, client):
        response = client.post(
            '/api/auth/forgot-password',
            json={'email': 'unknown@example.com'},
        )
        assert response.status_code == 404

    def test_reset_password_invalid_token(self, client):
        response = client.post(
            '/api/auth/reset-password',
            json={'token': 'wrongtoken', 'new_password': 'newpass123'},
        )
        assert response.status_code == 400

    def test_reset_password_missing_fields(self, client):
        response = client.post('/api/auth/reset-password', json={})
        assert response.status_code == 400

    def test_get_profile_requires_auth(self, client):
        response = client.get('/api/users/profile')
        assert response.status_code == 401

    def test_get_profile_success(self, app, client, customer_role):
        with app.app_context():
            user = UserModel(
                email='profile1@example.com',
                password_hash=generate_password_hash('123456'),
                full_name='Profile User',
                role_id=customer_role,
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        from flask_jwt_extended import create_access_token
        with app.app_context():
            token = create_access_token(identity=str(user_id))
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get('/api/users/profile', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == 'profile1@example.com'

    def test_update_profile_success(self, app, client, customer_role):
        with app.app_context():
            user = UserModel(
                email='update1@example.com',
                password_hash=generate_password_hash('123456'),
                full_name='Old Name',
                role_id=customer_role,
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        from flask_jwt_extended import create_access_token
        with app.app_context():
            token = create_access_token(identity=str(user_id))
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            '/api/users/profile',
            json={'full_name': 'New Name', 'phone': '0900000000'},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['full_name'] == 'New Name'
        assert data['phone'] == '0900000000'