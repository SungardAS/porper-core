
from porper.controllers.meta_resource_controller import MetaResourceController

class FunctionController(MetaResourceController):

    def __init__(self, connection=None):
        MetaResourceController.__init__(self, connection)
        from porper.models.function import Function
        self.function = Function(self.connection)
        from porper.models.permission import Permission
        self.permission = Permission(self.connection)
        from porper.models.function_permission import FunctionPermission
        self.function_permission = FunctionPermission(self.connection)


    def add_permission(self, function_id, permission):
        # create permission if not exists
        rows = self.permission.find_simple({'res_name': permission['resource']})
        if rows:
            permission = rows[0]
        else:
            permission = self.permission.create(
                {'res_name': permission['resource'], 'action': permission['action']}
            )

        # now add the map
        self.function_permission.create({'function_id': function_id, 'permission_id': permission['id']})


    def create(self, access_token, params):
        """
        possible attributes in params
            - name, list of permissions
            {"name": "Function name", "permissions": [{"resource": "user", "action": "r"}, ...]}
        """

        self.find_user_level(access_token)
        if not self.is_admin:
            raise Exception("not permitted")

        # find if the given function already exists
        rows = self.function.find_simple({"name": params['name']})
        if len(rows) > 0:
            print('already exists')
            return rows[0]['id']

        # create a function
        function = self.function.create({"name": params['name']})

        # add permissions to the function
        for permission in params['permissions']:
            self.add_permission(function['id'], permission)

        return function


    def delete(self, access_token, params):
        """
        possible attributes in params
            - id
        """

        self.find_user_level(access_token)
        if not self.is_admin:
            raise Exception("not permitted")

        if not params.get('id'):
            raise Exception("id must be provided")

        # remove the map
        self.function_permission.delete(function_id = params['id'])

        # remove this function
        return self.function.delete(params['id'])


    def update(self, access_token, params):
        """
        possible attributes in params
            - id, name, permission list
            {"id": "Function id", "name": "Function name", "permissions": [{"resource": "user", "action": "r"}, ...]}
        """

        self.find_user_level(access_token)
        if not self.is_admin:
            raise Exception("not permitted")

        if not params.get('id'):
            raise Exception("id must be provided")

        # find all permissions and add new ones
        if params.get('id'):
            rows = self.permission.find({"function_id": params['id']})
        if 'permissions' in params:
            for permission in params['permissions']:
                found = False
                for row in rows:
                    if permission['resource'] == row['res_name']:
                        found = True
                        row['found'] = found
                        break
                if not found:
                    self.add_permission(params['id'], permission)

            # delete old ones
            for row in rows:
                if 'found' not in row:
                    self.function_permission.delete({'function_id': params['id'], 'permission_id': row['id']})

        # update this function
        return self.function.update({"id": params['id'], "name": params['name']})


    def find(self, access_token, params):
        """
        possible attributes in params
            - id: find a specific function
            - None: No condition
        """

        self.find_user_level(access_token)
        if not self.is_admin:
            raise Exception("not permitted")

        if params.get("id"):
            function = self.function.find_by_id(params['id'])
            return function

        # in case there is no params
        function = {}
        for f in self.function.find({}):
            id = f['id']
            if id not in function:
                function[id] = {
                    'id': id,
                    'name': f['name'],
                    'permissions': [{'resource': f['p_resource_name'], 'action': f['p_action']}]
                }
            else:
                function[id]['permissions'].append({'resource': f['p_resource_name'], 'action': f['p_action']})
        return list(function.values())
