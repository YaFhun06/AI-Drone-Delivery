import os
import pytest
from src.create_app import create_app
from src.infrastructure.databases.base import db
from flask_jwt_extended import create_access_token


os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-secret'
os.environ['JWT_SECRET_KEY'] = 'test-secret'


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers():
    with create_app().app_context():
        token = create_access_token(identity='1')
    return {'Authorization': f'Bearer {token}'}
