
import json

ADMIN_ROLE_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'

class PermissionController:

    def __init__(self, connection):
        self.connection = connection
        from models.permission import Permission
        from models.user_role import UserRole
        self.permission = Permission(connection)
        self.user_role = UserRole(connection)
        from token_controller import TokenController
        self.token_controller = TokenController(connection)
        from user_role_controller import UserRoleController
        self.user_role_controller = UserRoleController(connection)

    def is_admin(self, user_id):
        row = self.user_role.find({'user_id': user_id, 'role_id': ADMIN_ROLE_ID})
        if len(row) > 0:  return True
        else: return False

    def is_role_admin(self, user_id, role_id):
        rows = self.user_role.find({'user_id': user_id, 'role_id': role_id})
        if len(rows) > 0 and rows[0]['is_admin']:  return True
        else: return False

    def are_permitted(self, access_token, params_list):
        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']
        for params in params_list:
            if not self.is_permitted(user_id, params):  return False
        return True

    def is_permitted(self, user_id, params):
        params['user_id'] = user_id
        params['all'] = True
        rows = self.permission.find(params)
        print "permitted : %s" % rows
        if len(rows) == 0:  return False
        for row in rows:
            if not row.get('condition'):   return True
        if not params.get('parent'):   return False    # parent must be given because all permissions have conditions
        # now check if the parent permissions include the given 'parent' value
        for row in rows:
            parent_params = json.loads(row['condition'])
            parent_params['user_id'] = user_id
            #parent_params['role_id'] = row['role_id']
            parent_params['value'] = params['parent']
            parent_params['all'] = True
            parent_rows = self.permission.find(parent_params)
            print "permitted parents : %s" % parent_rows
            if len(parent_rows) == 0:  return False     #### TODO: not sure if all have to be true......
        return True

    def create(self, access_token, params):
        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']
        if not self.is_admin(user_id):  raise Exception("not permitted")
        self.permission.create(params)
        return True

    def update(self, access_token, params):
        raise Exception("not supported")

    def delete(self, access_token, params):
        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']
        if not self.is_admin(user_id):  raise Exception("not permitted")
        self.permission.delete(params)
        return True

    """
    1. find all of my permissions from access_token
    2. find all permissions of given user if I'm the admin
    3. find all permissions of given role if I'm the admin
    4. find member's all permissions if I'm the role admin of the given role
    5. find member's all permissions if I'm the role admin of any roles where the given user belongs
    6. find member's all permissions if I'm the given user
    """
    def find_all(self, access_token, params):

        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']

        # return my permissions
        if not params.get('user_id') and not params.get('role_id'):
            params['user_id'] = user_id
            return self.permission.find(params)

        # return requested user/role's permissions if I'm an admin
        if self.is_admin(user_id):  return self.permission.find(params)

        # return requested role's permissions if I'm a role admin
        if params.get('role_id'):
            if self.is_role_admin(user_id, params['role_id']):  return self.permission.find(params)
            else:   raise Exception("not permitted")

        if params.get('user_id'):
            # return my permissions when the given user is me
            if user_id == params['user_id']:    return self.permission.find(params)

            # return requested user's permissions if I'm a role admin of any roles the given user belongs
            user_roles = self.user_role.find({'user_id': params['user_id']})
            if len(user_roles) == 0:    raise Exception("not permitted")
            for user_role in user_roles:
                if self.is_role_admin(user_id, user_role['role_id']):   return self.permission.find(params)
            raise Exception("not permitted")

    def find_one(self, access_token, params):
        raise Exception("not supported")
