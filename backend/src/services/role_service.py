from src.infrastructure.repositories.role_repository import RoleRepository

class RoleService:
    def __init__(self, role_repository: RoleRepository = None):
        self.role_repository = role_repository or RoleRepository()

    def list_roles(self):
        return self.role_repository.get_all()

    def create_role(self, name, description):
        return self.role_repository.create_role(name, description)

    def assign_function_to_role(self, role_id, function_id):
        return self.role_repository.assign_function(role_id, function_id)

    def list_functions(self):
        return self.role_repository.get_all_functions()