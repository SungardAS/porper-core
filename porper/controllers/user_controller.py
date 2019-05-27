
from porper.controllers.meta_resource_controller import MetaResourceController

class UserController(MetaResourceController):

    def __init__(self, connection):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.user import User
        from porper.models.user_group import UserGroup
        from porper.models.invited_user import InvitedUser
        self.user = User(connection)
        self.user_group = UserGroup(connection)
        self.invited_user = InvitedUser(connection)
        from porper.models.access_token import AccessToken
        self.access_token = AccessToken(connection)
        from porper.models.group import Group
        self.group = Group(connection)
        #from porper.controllers.token_controller import TokenController
        #self.token_controller = TokenController(connection)
        #from porper.controllers.permission_controller import PermissionController
        #self.permission_controller = PermissionController(self.connection)
        from porper.controllers.user_group_controller import UserGroupController
        self.user_group_controller = UserGroupController(self.connection)
        from porper.controllers.role_controller import RoleController
        self.role_controller = RoleController(self.connection)


    def create(self, access_token, params):
        """
        possible attributes in params
            - id, group_id, is_admin
            - id, email, auth_type, name, family_name and given_name
        """

        # if this is the first user, save it as an admin
        users = self.user.find({})
        if len(users) == 0:
            # set this user to the admin
            self.user.create(params)
            self.user_group.create({
                'user_id': params['id'],
                'group_id': self.ADMIN_GROUP_ID
            })
            return params['id']

        """# find current user information including id and level
        current_user = self.find_user_level(access_token, params.get('group_id'))

        # a normal user is not allowed
        if current_user['level'] == self.USER_LEVEL_USER:
            raise Exception('not permitted')"""

        # add the given user to the specified group
        if params.get("group_id"):
            """self.user_group.create({
                "user_id": params['id'],
                "group_id": current_user["group_id"],
                "is_admin": params['is_admin']
            })
            return params['id']"""
            return self.user_group_controller.create(
                access_token,
                {
                    "user_id": params['id'],
                    "group_id": params["group_id"],
                    "is_admin": params['is_admin']
                }
            )

        # find if the given user already exists
        rows = self.user.find({"email": params['email'], "auth_type": params['auth_type']})
        if len(rows) > 0:
            print('already exists')
            return rows[0]['id']

        # find if the given user is already invited
        invited_users = self.invited_user.find({'email':params['email'], 'auth_type':params['auth_type']})
        if len(invited_users) == 0:
            raise Exception("Please invite this user first")

        # add user_group_rel first to check the permission
        # if the current user is not admin and group admin, it will fail
        self.user_group_controller.create(
            access_token,
            {
                'user_id': params['id'],
                'group_id': invited_users[0]['group_id'],
                'is_admin': invited_users[0]['is_admin']
            }
        )

        # check if the current user is the admin of the invited user's group
        #if current_user['level'] != self.USER_LEVEL_ADMIN and not self.is_group_admin(current_user['user_id'], invited_users[0]['group_id']):
        #    raise Exception("Not permitted")

        # create a user and add it to the specified group
        self.user.create({
            'id': params['id'],
            'email': params['email'],
            'auth_type': params['auth_type'],
            'name': params['name'],
            'family_name': params['family_name'],
            'given_name': params['given_name'],
            'customer_id': params['customer_id']
        })
        self.invited_user.update({
            'email':params['email'],
            'auth_type':params['auth_type'],
            'state':self.invited_user.REGISTERED
        })
        return params['id']


    # now only remove the given user from a given group
    # it does NOT remove the given user from User table!!!!
    def delete(self, access_token, params):
        """
        possible attributes in params
            - id, group_id
        """
        removeuser=params.get('removeuser')
        if removeuser=="Y": 
           return self.user.delete(params['id'])
        if not params.get('id'):
            raise Exception("id must be provided")

        current_user = self.find_user_level(access_token, params['group_id'])

        if not params.get('group_id'):

            if current_user['level'] != self.USER_LEVEL_ADMIN:
                raise Exception("not permitted")

            # remove this user from all groups
            user_groups = self.user_group_controller.find(access_token, {'user_id': params['id']})
            for user_group in user_groups:
                self.user_group_controller.delete(access_token, user_group)

            # set this user's invite state to deleted
            user = self.user.find_by_id(params['id'])
            self.invited_user.find({'email':user['email'], 'auth_type':user['auth_type'], 'state':invited_user.DELETED})




        """if params['group_id'] == self.ADMIN_GROUP_ID:
            if current_user['level'] != self.USER_LEVEL_ADMIN:
                raise Exception("not permitted")
        elif current_user['level'] != self.USER_LEVEL_GROUP_ADMIN:
            raise Exception("not permitted")"""
        if current_user['level'] != self.USER_LEVEL_ADMIN and current_user['level'] != self.USER_LEVEL_GROUP_ADMIN:
            raise Exception("not permitted")

        user_groups = self.user_group_controller.find(access_token, {'group_id': params['group_id']})
        if params['group_id'] == self.ADMIN_GROUP_ID:
            if len(user_groups) == 1:
                raise Exception("You cannot remove this user because there must be at least one user in admin group")
        return self.user_group_controller.delete(
            access_token,
            {
                "user_id": params['id'],
                "group_id": params["group_id"]
            }
        )

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

        if params.get("detail") and params['detail']:
            return self.find_detail(access_token, params)

        ######### NOTICE
        #### When params has 'group_id', no other conditions cannot be used together!!!!
        if params.get("group_id"):
            #user_ids = self.user_group_controller.find(access_token, {'group_id': params['group_id']})
            #if len(user_ids) == 0:  return []
            user_groups = self.user_group_controller.find(access_token, {'group_id': params['group_id']})
            user_ids = [ user_group['user_id'] for user_group in user_groups ]
            if len(user_ids) == 0:  return []
            return self.add_groups(self.user.find_by_ids(user_ids))

        # find current user information including id and level
        current_user = self.find_user_level(access_token, params.get('group_id'))

        ######### NOTICE
        #### When params has 'id', no other conditions cannot be used together!!!!
        if params.get("id"):
            # it's me!
            if params['id'] == current_user['id']:
                return self.add_groups(self.user.find_by_id(params['id']))
            # if there is any group(s) where the current user and the given user belong together, return the given user info
            #group_ids = self.user_group_controller.find(access_token, {'user_id': params['id']})
            #if len(group_ids) == 0: raise Exception("not permitted")
            user_groups = self.user_group_controller.find(access_token, {'user_id': params['id']})
            if len(user_groups) == 0: raise Exception("not permitted")
            return self.add_groups(self.user.find_by_id(params['id']))

        ######### NOTICE
        #### When params has 'ids', no other conditions cannot be used together!!!!
        if params.get("ids"):
            user_groups = self.user_group_controller.find(access_token, {'user_ids': params['ids']})
            user_ids = [ user_group['user_id'] for user_group in user_groups ]
            if len(user_ids) == 0:  return []
            return self.add_groups(self.user.find_by_ids(user_ids))

        if not params:
            # in case there is no params
            users = self.user.find({})
        else:
            # for other parameters
            users = self.user.find(params)
        if current_user['level'] == self.USER_LEVEL_ADMIN:
            return self.add_groups(users)
        # return only the users who are in the same group with the current user among the returned users
        user_groups = self.user_group_controller.find(access_token, {'user_id': current_user['id']})
        group_ids = [ user_group['group_id'] for user_group in user_groups]
        user_groups = self.user_group_controller.find(access_token, {'group_ids': group_ids})
        user_ids = [ user_group['user_id'] for user_group in user_groups]
        return self.add_groups([ user for user in users if user['id'] in user_ids])


    def find_detail(self, access_token, params):
        current_users = self.access_token.find({'access_token': access_token})
        if not current_users:
            raise Exception("unauthorized")
        user_id = current_users[0]['user_id']
        current_user = self.user.find_by_id(user_id)
        user_groups = self.user_group_controller.find(access_token, {'user_id': user_id})
        group_ids = [ user_group['group_id'] for user_group in user_groups]
        groups = self.group.find_by_ids(group_ids)
        functions = []
        for group in groups:
            if group.get('role_id'):
                role = self.role_controller.find(access_token, {'id': group['role_id']})
                functions += role['functions']

        # remove duplicates
        unique_functions = []
        for function in functions:
            duplicates = [f["id"] for f in unique_functions if f["id"] == function["id"]]
            if duplicates:  continue
            unique_functions.append(function)

        current_user['groups'] = groups
        current_user['functions'] = unique_functions
        return current_user


    def add_groups(self, user):
        if isinstance(user, list):
            return self.add_groups_to_users(user)
        else:
            return self.add_groups_to_user(user)


    def add_groups_to_user(self, user):
        user_groups = self.user_group.find({'user_id': user['id']})
        group_ids = [ user_group['group_id'] for user_group in user_groups]
        groups = self.group.find_by_ids(group_ids)
        user['groups'] = groups
        return user

    def add_groups_to_users(self, users):
        ret_users = []
        for user in users:
            new_user = self.add_groups_to_user(user)
            ret_users.append(new_user)
        return ret_users
