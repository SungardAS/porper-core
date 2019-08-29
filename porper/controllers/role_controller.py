
from porper.controllers.meta_resource_controller import MetaResourceController

class RoleController(MetaResourceController):

    def __init__(self, connection=None):
        MetaResourceController.__init__(self, connection)
        from porper.models.role import Role
        self.role = Role(self.connection)
        from porper.models.role_function import RoleFunction
        self.role_function = RoleFunction(self.connection)
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
        role_params = {'name': params['name']}
        if 'id' in params:
            role_params['id'] = params['id']
        ret = self.role.create(role_params)

        for function in params['functions']:
            self.role_function.create({'role_id': ret['id'], 'function_id': function})

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

        self.role_function.delete(role_id=params['id'])

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

        functions = [rf['function_id'] for rf in self.role_function.find_simple({'role_id': params['id']})]
        for nf in params['functions']:
            if nf not in functions:
                self.role_function.create({"role_id": params['id'], 'function_id': nf})
        for of in functions:
            if of not in params['functions']:
                self.role_function.delete(role_id=params['id'], function_id=of)

        # update this role
        self.role.update({'id': params['id'], 'name': params['name']})

        return params


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
            ret = self.role.find(params)
        elif self.is_customer_admin:
            ret = self.role.find(params, customer_id=self.customer_id)
        else:
            ret = self.role.find(params, user_id=self.user_id)

        # build permissions by function
        f_permission = {}
        for r in ret:
            function_id = r['function_id']
            if function_id:
                if function_id not in f_permission:
                    f_permission[function_id] = [{'resource': r['resource_name'], 'action': r['action']}]
                else:
                    found = False
                    for p in f_permission[function_id]:
                        if p['resource'] == r['resource_name'] and p['action'] == r['action']:
                            found = True
                            break
                    if not found:
                        f_permission[function_id].append({'resource': r['resource_name'], 'action': r['action']})

        # now build functions by role
        role = {}
        for r in ret:
            role_id = r['role_id']
            function_id = r['function_id']
            if role_id not in role:
                role[role_id] = {
                    'id': role_id,
                    'name': r['role_name']
                }
                if function_id:
                    role[role_id]['functions'] = [{'id': function_id, 'name': r['function_name'], 'permissions': f_permission.get(function_id)}]
                else:
                    role[role_id]['functions'] = []
            else:
                if function_id:
                    found = False
                    for f in role[role_id]['functions']:
                        if f['id'] == function_id:
                            found = True
                            break
                    if not found:
                        role[role_id]['functions'].append({'id': function_id, 'name': r['function_name'], 'permissions': f_permission.get(function_id)})

        ret = list(role.values())

        if ret and 'id' in params:
            return ret[0]

        return ret

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
