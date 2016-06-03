
import sys
sys.path.insert(0, r'..')

ADMIN_ROLE_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'

class RoleController:

    def __init__(self, region, connection):
        self.region = region
        self.connection = connection

        if connection:
            from models.role import Role
            from models.user_role import UserRole
            self.role = Role(connection)
            self.user_role = UserRole(connection)
        else:
            from models_d.role import Role
            from models_d.user_role import UserRole
            self.role = Role(region)
            self.user_role = UserRole(region)

        from access_token_controller import AccessTokenController
        self.access_token_controller = AccessTokenController(region, connection)
        from user_role_controller import UserRoleController
        self.user_role_controller = UserRoleController(region, connection)

    def is_admin(self, user_id):
        row = self.user_role.find({'user_id': user_id, 'role_id': ADMIN_ROLE_ID})
        if len(row) > 0:  return True
        else: return False

    # only the admin can create a role
    def create(self, access_token, params):
        rows = self.access_token_controller.find(access_token)
        user_id = rows[0]['user_id']
        if not self.is_admin(user_id):  raise Exception("not permitted")
        self.role.create(params)
        return True

    def update(self, access_token, params):
        raise Exception("not supported")

    def delete(self, access_token, params):
        raise Exception("not supported")

    """
    1. find all roles if I'm the admin
    2. find only roles where I'm the role admin
    """
    def find_all(self, access_token, params=None):
        rows = self.access_token_controller.find(access_token)
        user_id = rows[0]['user_id']
        return self.user_role_controller.find_by_user_id(user_id)

    def find_one(self, access_token, params):
        raise Exception("not supported")
