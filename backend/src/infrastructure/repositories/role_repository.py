from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.models.auth_function_model import AuthFunctionModel
from src.infrastructure.models.auth_role_function_model import AuthRoleFunctionModel
from src.infrastructure.databases.base import db

class RoleRepository:
    def get_all(self):
        return RoleModel.query.all()

    def create_role(self, name, description):
        role = RoleModel(name=name, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    def find_by_id(self, role_id):
        return RoleModel.query.get(role_id)

    def assign_function(self, role_id, function_id):
        existing = AuthRoleFunctionModel.query.filter_by(role_id=role_id, function_id=function_id).first()
        if existing:
            return existing
        mapping = AuthRoleFunctionModel(role_id=role_id, function_id=function_id)
        db.session.add(mapping)
        db.session.commit()
        return mapping

    def get_all_functions(self):
        return AuthFunctionModel.query.all()