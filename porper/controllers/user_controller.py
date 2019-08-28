
from porper.controllers.meta_resource_controller import MetaResourceController

class UserController(MetaResourceController):

    def __init__(self, connection=None):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.user import User
        self.user = User(self.connection)
        from porper.models.user_group import UserGroup
        self.user_group = UserGroup(self.connection)
        from porper.models.invited_user import InvitedUser
        self.invited_user = InvitedUser(self.connection)
        from porper.models.customer import Customer
        self.customer = Customer(self.connection)
        from porper.models.access_token import AccessToken
        self.access_token = AccessToken(self.connection)
        from porper.models.function import Function
        self.function = Function(self.connection)
        # from porper.models.group import Group
        # self.group = Group(connection)
        #from porper.controllers.token_controller import TokenController
        #self.token_controller = TokenController(self.connection)
        #from porper.controllers.permission_controller import PermissionController
        #self.permission_controller = PermissionController(self.connection)
        # from porper.controllers.user_group_controller import UserGroupController
        # self.user_group_controller = UserGroupController(self.connection)
        # from porper.controllers.role_controller import RoleController
        # self.role_controller = RoleController(self.connection)

        self.permission_name = "user"


    def create(self, access_token, params):
        """
        possible attributes in params
            - id, group_id, is_admin
            - id, email, auth_type, name, family_name and given_name
        """

        # # if this is the first user, save it as an admin
        # users = self.user.find({})
        # if len(users) == 0:
        #     # set this user to the admin
        #     self.user.create(params)
        #     from porper.models.group import Group
        #     group = Group(self.dynamodb)
        #     admin_groups = group.find_admin_groups()
        #     if not admin_groups:
        #         raise Exception("No admin group found")
        #     self.user_group.create({
        #         'user_id': params['id'],
        #         'group_id': admin_groups[0]['id']
        #     })
        #     return params['id']

        # find current user information including id and level
        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        if not self.is_member(group_id=params['group_id']):
            raise Exception("not permitted")

        # add the given user to the specified group
        return self.user_group.create(
            {
                "user_id": params['id'],
                "group_id": params["group_id"]
            }
        )

        # # find if the given user already exists
        # rows = self.user.find({"email": params['email'], "auth_type": params['auth_type']})
        # if len(rows) > 0:
        #     print('already exists')
        #     return rows[0]['id']
        #
        # # find if the given user is already invited
        # invited_users = self.invited_user.find({'email':params['email'], 'auth_type':params['auth_type']})
        # if len(invited_users) == 0:
        #     raise Exception("Please invite this user first")
        #
        # # add user_group_rel first to check the permission
        # # if the current user is not admin and group admin, it will fail
        # self.user_group_controller.create(
        #     access_token,
        #     {
        #         'user_id': params['id'],
        #         'group_id': invited_users[0]['group_id'],
        #         'is_admin': invited_users[0]['is_admin']
        #     }
        # )
        #
        # # check if the current user is the admin of the invited user's group
        # #if current_user['level'] != self.USER_LEVEL_ADMIN and not self.is_group_admin(current_user['user_id'], invited_users[0]['group_id']):
        # #    raise Exception("Not permitted")
        #
        # # create a user and add it to the specified group
        # self.user.create({
        #     'id': params['id'],
        #     'email': params['email'],
        #     'auth_type': params['auth_type'],
        #     'name': params['name'],
        #     'family_name': params['family_name'],
        #     'given_name': params['given_name'],
        #     'customer_id': params['customer_id']
        # })
        # self.invited_user.update({
        #     'email':params['email'],
        #     'auth_type':params['auth_type'],
        #     'state':self.invited_user.REGISTERED
        # })
        # return params['id']


    # def delete_access_tokens(self, access_token, user_id):
    #     # Remove the access tokens of the user that is being deleted
    #     # access_token_rows = self.access_token.find({"user_id": params['id']})
    #     # print("Access Tokens found")
    #     # if len(access_token_rows) > 0:
    #     #     for acctoken in access_token_rows:
    #     #         access_token_id=acctoken.get('access_token')
    #     #         print(access_token_id)
    #     #         self.access_token.delete(access_token_id)
    #     self.find_user_level(access_token)
    #     if self.is_permitted(self.permission_name, self.permission_write)
    #         raise Exception("not permitted")
    #
    #     # find the group where the given user belongs
    #     rows = self.user_group.find_groups([user_id])
    #
    #
    #
    #
    #     return self.access_token.delete_by_user(user_id)


    # now only remove the given user from a given group
    # it does NOT remove the given user from User table!!!!
    def delete(self, access_token, params):
        """
        possible attributes in params
            - id, group_id
        """
        self.find_user_level(access_token)
        if self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        if not params.get('id'):
           raise Exception("id must be provided")

        if 'group_id' not in params:
            # find the customer_id of this given user
            items = self.customer.find({'user_id': id})
            if not items or not self.is_member(customer_id=items[0]['id']):
                raise Exception("not permitted")

            # find user info before removing it
            user_info = self.user.find_by_id(params['id'])

            # remove this user from all groups
            self.user_group.delete(user_id=params['id'])

            # set this user's invite state to deleted
            self.invited_user.update_state(user_info['email'], user_info['auth_type'], self.invited_user.DELETED)

        else:
            if not self.is_member(group_id=params['group_id']):
                raise Exception("not permitted")
            return self.user_group.delete(user_id=params['id'], group_id=params["group_id"])

        # removeuser=params.get('removeuser')
        # if removeuser=="Y":
        #     # remove this user from all groups
        #     user_groups = self.user_group_controller.find(access_token, {'user_id': params['id']})
        #     for user_group in user_groups:
        #         self.user_group_controller.delete(access_token, user_group)
        #         # set this user's invite state to deleted
        #     user = self.user.find_by_id(params['id'])
        #     # find if the given user already exists
        #     # Remove the access tokens of the user that is being deleted
        #     access_token_rows = self.access_token.find({"user_id": params['id']})
        #     print("Access Tokens found")
        #     if len(access_token_rows) > 0:
        #         for acctoken in access_token_rows:
        #             access_token_id=acctoken.get('access_token')
        #             print(access_token_id)
        #             self.access_token.delete(access_token_id)
        #
        #     #self.invited_user.delete({'email': params['email'], 'auth_type': params['auth_type']})
        #     return self.user.delete(params['id'])


        # user_groups = self.user_group_controller.find(access_token, {'group_id': params['group_id']})
        # if params['group_id'] == self.ADMIN_GROUP_ID:
        #     if len(user_groups) == 1:
        #         raise Exception("You cannot remove this user because there must be at least one user in admin group")

        ###TODO: remove all permissions assigned to this user!!!!


    """def find_buddy_ids(self, user_id):
         user_groups = self.user_group.find({'user_id': user_id})
         group_ids = [ user_group['group_id'] for user_group in user_groups ]
         user_groups = self.user_group.find_by_group_ids(group_ids)
         user_ids = [ user_group['user_id'] for user_group in user_groups ]
         return user_ids"""


    def find(self, access_token, params):
        """
        possible attributes in params
            - detail: find all groups and functions of the current user
            - group_id: find all users in this given group
            - id: find a specific user
            - ids: find specific users
            - None: No condition
            - any combination of email, auth_type, name, family_name and given_name
        """

        self.find_user_level(access_token)

        if params.get("detail"):
            return self.find_detail(access_token, params)

        # This is to get information of myself
        if params.get("id") and self.user_id == params['id']:
            params['user_id'] = params['id']
            del params['id']
            return self.user.find(params, user_id=self.user_id)

        if not self.is_permitted(self.permission_name, self.permission_read):
            raise Exception("not permitted")

        ######### NOTICE
        #### When params has 'ids', no other conditions cannot be used together!!!!
        if params.get("ids"):
            if self.is_admin:
                ret = self.user.find_by_ids(self.params['ids'])
            elif self.is_customer_admin:
                ret = self.user.find_by_ids(self.params['ids'], customer_id=self.customer_id)
            else:
                ret = self.user.find_by_ids(self.params['ids'], user_id=self.user_id)

        else:
            if self.is_admin:
                ret = self.user.find(params)
            elif self.is_customer_admin:
                ret = self.user.find(params, customer_id=self.customer_id)
            else:
                ret = self.user.find(params, user_id=self.user_id)

        user = {}
        for u in ret:
            id = u['id']
            if id not in user:
                user[id] = {
                    'id': id,
                    "email": u['email'],
                    "customer_id": u['customer_id'],
                    "family_name": u['family_name'],
                    "given_name": u['given_name'],
                    "name": u['name'],
                    "auth_type": u['auth_type'],
                    'groups': [
                        {
                            'id': u['group_id'],
                            'name': u['group_name'],
                            'customer_id': u['customer_id'],
                            'role_id': u['role_id']
                        }
                    ]
                }
            else:
                user[id]['groups'].append(
                    {
                        'id': u['group_id'],
                        'name': u['group_name'],
                        'customer_id': u['customer_id'],
                        'role_id': u['role_id']
                    }
                )
        return list(user.values())


        # ######### NOTICE
        # #### When params has 'group_id', no other conditions cannot be used together!!!!
        # if params.get("group_id"):
        #     # #user_ids = self.user_group_controller.find(access_token, {'group_id': params['group_id']})
        #     # #if len(user_ids) == 0:  return []
        #     # user_groups = self.user_group_controller.find(access_token, {'group_id': params['group_id']})
        #     # user_ids = [ user_group['user_id'] for user_group in user_groups ]
        #     # if len(user_ids) == 0:  return []
        #     # return self.add_groups(self.user.find_by_ids(user_ids))

        # ######### NOTICE
        # #### When params has 'id', no other conditions cannot be used together!!!!
        # if params.get("id"):
        #     # it's me!
        #     if params['id'] == current_user['id']:
        #         return self.add_groups(self.user.find_by_id(params['id']))
        #     # if there is any group(s) where the current user and the given user belong together, return the given user info
        #     #group_ids = self.user_group_controller.find(access_token, {'user_id': params['id']})
        #     #if len(group_ids) == 0: raise Exception("not permitted")
        #     user_groups = self.user_group_controller.find(access_token, {'user_id': params['id']})
        #     if len(user_groups) == 0: raise Exception("not permitted")
        #     return self.add_groups(self.user.find_by_id(params['id']))
        #
        #
        # if not params:
        #     # in case there is no params
        #     users = self.user.find({})
        # else:
        #     # for other parameters
        #     users = self.user.find(params)
        # if current_user['level'] == self.USER_LEVEL_ADMIN:
        #     return self.add_groups(users)
        # # return only the users who are in the same group with the current user among the returned users
        # user_groups = self.user_group_controller.find(access_token, {'user_id': current_user['id']})
        # group_ids = [ user_group['group_id'] for user_group in user_groups]
        # user_groups = self.user_group_controller.find(access_token, {'group_ids': group_ids})
        # user_ids = [ user_group['user_id'] for user_group in user_groups]
        # return self.add_groups([ user for user in users if user['id'] in user_ids])


    def find_detail(self, access_token, params):

        # current_users = self.access_token.find({'access_token': access_token})
        # if not current_users:
        #     raise Exception("unauthorized")
        # user_id = current_users[0]['user_id']
        # current_user = self.user.find_by_id(user_id)
        user = self.access_token.find_user(access_token)
        if not user:
            raise Exception("not unauthorized")

        user['groups'] = self.group.find({'user_id': self.user_id})
        user['customer_id'] = user['groups'][0]['customer_id']

        function = {}
        for f in self.function.find({'user_id': self.user_id}):
            id = f['id']
            if id not in function:
                function[id] = {
                    'id': id,
                    'name': f['name'],
                    'permissions': [{'resource': f['p_resource_name'], 'action': f['p_action']}]
                }
            else:
                function[id]['permissions'].append({'resource': f['p_resource_name'], 'action': f['p_action']})
        user['functions'] = list(function.values())

        # user_groups = self.user_group_controller.find(access_token, {'user_id': user_id})
        # if user_groups:
        #     group_ids = [ user_group['group_id'] for user_group in user_groups]
        #     groups = self.group.find_by_ids(group_ids)
        #     functions = []
        #     for group in groups:
        #         if group.get('role_id'):
        #             role = self.role_controller.find(access_token, {'id': group['role_id']})
        #             functions += role['functions']
        #
        #     # remove duplicates
        #     unique_functions = []
        #     for function in functions:
        #         duplicates = [f["id"] for f in unique_functions if f["id"] == function["id"]]
        #         if duplicates:  continue
        #         unique_functions.append(function)
        # else:
        #     groups = []
        #     unique_functions = []
        #
        # current_user['groups'] = groups
        # current_user['functions'] = unique_functions
        return user


    # def add_groups(self, user):
    #     if isinstance(user, list):
    #         return self.add_groups_to_users(user)
    #     else:
    #         return self.add_groups_to_user(user)
    #
    #
    # def add_groups_to_user(self, user):
    #     user_groups = self.user_group.find({'user_id': user['id']})
    #     if user_groups:
    #         group_ids = [ user_group['group_id'] for user_group in user_groups]
    #         groups = self.group.find_by_ids(group_ids)
    #         user['groups'] = groups
    #     else:
    #         user['groups'] = []
    #     return user
    #
    # def add_groups_to_users(self, users):
    #     ret_users = []
    #     for user in users:
    #         new_user = self.add_groups_to_user(user)
    #         ret_users.append(new_user)
    #     return ret_users
