
from porper.controllers.meta_resource_controller import MetaResourceController

class RoleController(MetaResourceController):

    def __init__(self, connection):
        MetaResourceController.__init__(self, connection)
        from porper.models.role import Role
        self.role = Role(connection)
        from porper.models.function import Function
        self.function = Function(connection)
        from porper.controllers.user_group_controller import UserGroupController
        self.user_group_controller = UserGroupController(self.connection)
        from porper.controllers.token_controller import TokenController
        self.token_controller = TokenController(self.connection)
        from porper.models.group import Group
        self.group = Group(connection)


    def create(self, access_token, params):
        """
        possible attributes in params
            - name, list of functions
            {"name": "Role name", "functions": [id1, id2, id3.....]}
        """

        current_user = self.find_user_level(access_token)
        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception("not permitted")

        # find if the given role already exists
        rows = self.role.find({"name": params['name']})
        if len(rows) > 0:
            print('already exists')
            return rows[0]['id']

        # create a role
        params = self.role.create(params)
        return params


    def delete(self, access_token, params):
        """
        possible attributes in params
            - id
        """

        if not params.get('id'):
            raise Exception("id must be provided")

        current_user = self.find_user_level(access_token)
        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception("not permitted")

        # remove this role
        return self.role.delete(params['id'])


    def update(self, access_token, params):
        """
        possible attributes in params
            - id, name, function list
            {"id": "Role id", "name": "Role name", "functions": [id1, id2, id3.....]}
        """

        if not params.get('id'):
            raise Exception("id must be provided")

        current_user = self.find_user_level(access_token)
        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception("not permitted")

        # update this role
        return self.role.update(params)


    def find(self, access_token, params):
        """
        possible attributes in params
            - id: find a specific role
            - None: No condition
        """

        current_user = self.find_user_level(access_token)

        if params.get("id"):
            # check if this role is permitted to this user
            user_id = self.token_controller.find_user_id(access_token)
            user_groups = self.user_group_controller.find(access_token, {'user_id': user_id})
            group_ids = [ user_group['group_id'] for user_group in user_groups]
            groups = self.group.find_by_ids(group_ids)
            role_ids = [group['role_id'] for group in groups if group['role_id'] == params['id']]
            if not role_ids:
                raise Exception("not permitted")

            role = self.role.find_by_id(params['id'])
            functions = self.validate_functions(role['functions'])
            role['functions'] = functions
            return role

        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception("not permitted")

        if params:
            roles = self.role.find(params)
        else:
            # in case there is no params
            roles = self.role.find({})

        for role in roles:
            functions = self.validate_functions(role['functions'])
            role['functions'] = functions
        return roles


    def validate_functions(self, function_ids):
        valids = []
        for id in function_ids:
            function = self.function.find_by_id(id)
            if function:
                valids.append(function)
        return valids
