from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.databases.base import db

class UserRepository:
    def find_by_email(self, email):
        return UserModel.query.filter_by(email=email).first()

    def find_role_by_name(self, name):
        return RoleModel.query.filter_by(name=name).first()

    def create_user(self, email, password_hash, full_name, role_id):
        user = UserModel(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role_id=role_id
        )
        db.session.add(user)
        db.session.commit()
        return user

    def update_reset_token(self, user, token, expiry):
        user.reset_token = token
        user.reset_token_expiry = expiry
        db.session.commit()

    def find_by_reset_token(self, token):
        return UserModel.query.filter_by(reset_token=token).first()

    def update_password(self, user, new_password_hash):
        user.password_hash = new_password_hash
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

    def find_by_id(self, user_id):
        return UserModel.query.get(user_id)

    def update_profile(self, user, full_name=None, phone=None):
        if full_name is not None:
            user.full_name = full_name
        if phone is not None:
            user.phone = phone
        db.session.commit()
        return user