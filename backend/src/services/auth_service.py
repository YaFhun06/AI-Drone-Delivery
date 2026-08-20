from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.exceptions import (
    EmailAlreadyExistsError,
    RoleNotConfiguredError,
    InvalidCredentialsError,
    AccountLockedError,
)


class AuthService:
    def __init__(self, user_repository: UserRepository = None):
        self.user_repository = user_repository or UserRepository()

    def register(self, email, password, full_name):
        if self.user_repository.find_by_email(email):
            raise EmailAlreadyExistsError()

        customer_role = self.user_repository.find_role_by_name("Customer")
        if not customer_role:
            raise RoleNotConfiguredError()

        hashed_password = generate_password_hash(password)
        return self.user_repository.create_user(
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            role_id=customer_role.id,
        )

    def login(self, email, password):
        user = self.user_repository.find_by_email(email)

        if not user or not check_password_hash(user.password_hash, password):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise AccountLockedError()

        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token, "user": user}