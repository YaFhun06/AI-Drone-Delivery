from src.infrastructure.databases.base import db
from sqlalchemy import UniqueConstraint

class AuthRoleFunctionModel(db.Model):
    __tablename__ = 'auth_role_functions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    function_id = db.Column(db.Integer, db.ForeignKey('auth_functions.id'), nullable=False)

    __table_args__ = (UniqueConstraint('role_id', 'function_id', name='uq_role_function'),)

    def __repr__(self):
        return f"<AuthRoleFunctionModel(role_id='{self.role_id}', function_id='{self.function_id}')>"