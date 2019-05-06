
from porper.controllers.meta_resource_controller import MetaResourceController

class FunctionController(MetaResourceController):

    def __init__(self, connection):
        MetaResourceController.__init__(self, connection)
        from porper.models.function import Function
        self.function = Function(connection)


    def create(self, access_token, params):
        """
        possible attributes in params
            - name, list of permissions
            {"name": "Function name", "permissions": [{"resource_name": "resource name", "permissions": "rw|r|w"}, ...]}
        """

        current_user = self.find_user_level(access_token)
        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception("not permitted")

        # find if the given function already exists
        rows = self.function.find({"name": params['name']})
        if len(rows) > 0:
            print('already exists')
            return rows[0]['id']

        # create a function
        params = self.function.create(params)
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

        # remove this function
        return self.function.delete(params['id'])


    def update(self, access_token, params):
        """
        possible attributes in params
            - id, name, permission list
            {"id": "Function id", "name": "Function name", "permissions": [{"resource_name": "resource name", "permissions": "rw|r|w"}, ...]}
        """

        if not params.get('id'):
            raise Exception("id must be provided")

        current_user = self.find_user_level(access_token)
        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception("not permitted")

        # update this function
        return self.function.update(params)


    def find(self, access_token, params):
        """
        possible attributes in params
            - id: find a specific function
            - None: No condition
        """

        current_user = self.find_user_level(access_token)
        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception("not permitted")

        if params.get("id"):
            function = self.function.find_by_id(params['id'])
            return function

        # in case there is no params
        functions = self.function.find({})
        return functions
