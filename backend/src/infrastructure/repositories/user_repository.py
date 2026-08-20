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