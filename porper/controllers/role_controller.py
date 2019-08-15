
from porper.controllers.meta_resource_controller import MetaResourceController

class RoleController(MetaResourceController):

    def __init__(self, connection=None):
        MetaResourceController.__init__(self, connection)
        from porper.models.role import Role
        self.role = Role(self.connection)
        # from porper.models.function import Function
        # self.function = Function(self.connection)
        # from porper.controllers.user_group_controller import UserGroupController
        # self.user_group_controller = UserGroupController(self.connection)
        # from porper.controllers.token_controller import TokenController
        # self.token_controller = TokenController(self.connection)
        # from porper.models.group import Group
        # self.group = Group(self.connection)

        self.permission_name = "role"


    def create(self, access_token, params):
        """
        possible attributes in params
            - name, list of functions
            {"name": "Role name", "functions": [id1, id2, id3.....]}
        """

        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_write):
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

        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        if not params.get('id'):
            raise Exception("id must be provided")

        # remove this role
        return self.role.delete(params['id'])


    def update(self, access_token, params):
        """
        possible attributes in params
            - id, name, function list
            {"id": "Role id", "name": "Role name", "functions": [id1, id2, id3.....]}
        """

        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        if not params.get('id'):
            raise Exception("id must be provided")

        # update this role
        return self.role.update(params)


    def find(self, access_token, params):
        """
        possible attributes in params
            - id: find a specific role
            - None: No condition
        """

        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_read):
            raise Exception("not permitted")

        if self.is_admin:
            return self.role.find(params)
        if self.is_customer_admin:
            return self.role.find(params, customer_id=current_user.customer_id)
        else:
            return self.role.find(params, user_id=current_user.user_id)

        # if params.get("id"):
        #     if current_user['level'] != self.USER_LEVEL_ADMIN:
        #         # check if this role is permitted to this user
        #         user_id = self.token_controller.find_user_id(access_token)
        #         user_groups = self.user_group_controller.find(access_token, {'user_id': user_id})
        #         group_ids = [ user_group['group_id'] for user_group in user_groups]
        #         print(group_ids)
        #         groups = self.group.find_by_ids(group_ids)
        #         print(groups)
        #         role_ids = [group['role_id'] for group in groups if group['role_id'] == params['id']]
        #         if not role_ids:
        #             raise Exception("not permitted")
        #
        #     role = self.role.find_by_id(params['id'])
        #     functions = self.validate_functions(role['functions'])
        #     role['functions'] = functions
        #     return role
        #
        # if current_user['level'] != self.USER_LEVEL_ADMIN:
        #     raise Exception("not permitted")
        #
        # if params:
        #     roles = self.role.find(params)
        # else:
        #     # in case there is no params
        #     roles = self.role.find({})
        #
        # for role in roles:
        #     functions = self.validate_functions(role['functions'])
        #     role['functions'] = functions
        # return roles


    # def validate_functions(self, function_ids):
    #     valids = []
    #     for id in function_ids:
    #         function = self.function.find_by_id(id)
    #         if function:
    #             valids.append(function)
    #     return valids
