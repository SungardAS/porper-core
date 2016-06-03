
import sys
sys.path.insert(0, r'..')

ADMIN_ROLE_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'

class UserController:

    def __init__(self, region, connection):
        self.region = region
        self.connection = connection

        if connection:
            from models.user import User
            from models.user_role import UserRole
            self.user = User(connection)
            self.user_role = UserRole(connection)
        else:
            from models_d.user import User
            from models_d.user_role import UserRole
            self.user = User(region)
            self.user_role = UserRole(region)

        from access_token_controller import AccessTokenController
        self.access_token_controller = AccessTokenController(region, connection)

    def is_admin(self, user_id):
        row = self.user_role.find({'user_id': user_id, 'role_id': ADMIN_ROLE_ID})
        if len(row) > 0:  return True
        else: return False

    def is_role_admin(self, user_id, role_id):
        rows = self.user_role.find({'user_id': user_id, 'role_id': role_id})
        if len(rows) > 0 and rows[0]['is_admin']:  return True
        else: return False

    def is_member(self, user_id, role_id):
        rows = self.user_role.find({'user_id': user_id, 'role_id': role_id})
        if len(rows) > 0:  return True
        else: return False

    # anyone who successfully logs in can save its information
    def create(self, access_token, params):
        if params.get('role_id'):
            rows = self.access_token_controller.find(access_token)
            user_id = rows[0]['user_id']
            # add this user to the given role only if I'm the admin or the role admin of the role
            if self.is_admin(user_id) or self.is_role_admin(user_id, role_id):
                if params.get('is_admin') == None:
                    params['is_admin'] = False
                return self.user_role.create(params)
            else:
                raise Exception("not permitted")
        else:
            return self.save(params['id'], params['family_name'], params['given_name'], params['email'])

    # anyone who successfully logs in can save its information
    def save(self, id, family_name, given_name, email):
        params = {
          'id': id,
          'family_name': family_name,
          'given_name': given_name,
          'email': email
        }
        rows = self.user.find(params)
        if len(rows) > 0:
            print 'already exists'
            return
        return self.user.create(params)

    """
    1. return requested users if I'm the admin
    2. return all users of roles where I'm the role admin
    3. return myself if I'm not the role admin of any role
    4. return all members of the given role if I'm a member of the given role
    """
    def find_all(self, access_token, params):

        rows = self.access_token_controller.find(access_token)
        user_id = rows[0]['user_id']

        # return all users if I'm an admin
        if self.is_admin(user_id):  return self.user.find(params)

        if not params.get('role_id'):
            # return all users of roles where I'm the role admin
            user_roles = self.user_role.find({'user_id': user_id})
            role_ids = [ user_role['role_id'] for user_role in user_roles if user_role['is_admin'] ]
            if len(role_ids) > 0:   return self.user.find({'role_ids': role_ids})

            # if role is not given, return only itself
            return self.user.find({'id': user_id})

        # return all members of the given role if I'm a member of the given role
        if self.is_member(user_id, params['role_id']):  return self.user.find(params)

        raise Exception("not permitted")
