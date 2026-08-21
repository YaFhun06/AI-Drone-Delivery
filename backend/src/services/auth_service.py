from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
import random

from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.exceptions import (
    EmailAlreadyExistsError,
    RoleNotConfiguredError,
    InvalidCredentialsError,
    AccountLockedError,
    InvalidResetTokenError,
    UserNotFoundError,
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

    def forgot_password(self, email):
        user = self.user_repository.find_by_email(email)
        if not user:
            raise UserNotFoundError()

        reset_code = str(random.randint(100000, 999999))
        expiry = datetime.utcnow() + timedelta(minutes=15)
        self.user_repository.update_reset_token(user, reset_code, expiry)

        print(f"[RESET PASSWORD] Gửi tới {email}: mã xác nhận là {reset_code}")

        return reset_code

    def reset_password(self, token, new_password):
        user = self.user_repository.find_by_reset_token(token)

        if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
            raise InvalidResetTokenError()

        hashed_password = generate_password_hash(new_password)
        self.user_repository.update_password(user, hashed_password)

    def get_profile(self, user_id):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    def update_profile(self, user_id, full_name=None, phone=None):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return self.user_repository.update_profile(user, full_name, phone)