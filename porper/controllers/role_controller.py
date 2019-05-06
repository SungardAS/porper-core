
from porper.controllers.meta_resource_controller import MetaResourceController

class RoleController(MetaResourceController):

    def __init__(self, connection):
        MetaResourceController.__init__(self, connection)
        from porper.models.role import Role
        self.role = Role(connection)
        from porper.models.function import Function
        self.function = Function(connection)


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
        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception("not permitted")

        if params.get("id"):
            role = self.role.find_by_id(params['id'])
            functions = self.validate_functions(role['functions'])
            role['functions'] = functions
            return role

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
