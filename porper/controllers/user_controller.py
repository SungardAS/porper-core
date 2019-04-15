
from porper.controllers.meta_resource_controller import MetaResourceController

class UserController(MetaResourceController):

    def __init__(self, connection):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.user import User
        #from porper.models.user_group import UserGroup
        from porper.models.invited_user import InvitedUser
        self.user = User(connection)
        #self.user_group = UserGroup(connection)
        self.invited_user = InvitedUser(connection)
        #from porper.controllers.token_controller import TokenController
        #self.token_controller = TokenController(connection)
        #from porper.controllers.permission_controller import PermissionController
        #self.permission_controller = PermissionController(self.connection)
        from porper.controllers.user_group_controller import UserGroupController
        self.user_group_controller = UserGroupController(self.connection)


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
            'given_name': params['given_name']
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

        if not params.get('id') or not params.get('group_id'):
            raise Exception("both id and group_id must be provided")

        current_user = self.find_user_level(access_token, params['group_id'])

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
            - group_id: find all users in this given group
            - id: find a specific user
            - ids: find specific users
            - None: No condition
            - any combination of email, auth_type, name, family_name and given_name
        """

        ######### NOTICE
        #### When params has 'group_id', no other conditions cannot be used together!!!!
        if params.get("group_id"):
            #user_ids = self.user_group_controller.find(access_token, {'group_id': params['group_id']})
            #if len(user_ids) == 0:  return []
            user_groups = self.user_group_controller.find(access_token, {'group_id': params['group_id']})
            user_ids = [ user_group['user_id'] for user_group in user_groups ]
            if len(user_ids) == 0:  return []
            return self.user.find_by_ids(user_ids)

        # find current user information including id and level
        current_user = self.find_user_level(access_token, params.get('group_id'))

        ######### NOTICE
        #### When params has 'id', no other conditions cannot be used together!!!!
        if params.get("id"):
            # it's me!
            if params['id'] == current_user['id']:
                return self.user.find_by_id(params['id'])
            # if there is any group(s) where the current user and the given user belong together, return the given user info
            #group_ids = self.user_group_controller.find(access_token, {'user_id': params['id']})
            #if len(group_ids) == 0: raise Exception("not permitted")
            user_groups = self.user_group_controller.find(access_token, {'user_id': params['id']})
            if len(user_groups) == 0: raise Exception("not permitted")
            return self.user.find_by_id(params['id'])

        ######### NOTICE
        #### When params has 'ids', no other conditions cannot be used together!!!!
        if params.get("ids"):
            user_groups = self.user_group_controller.find(access_token, {'user_ids': params['ids']})
            user_ids = [ user_group['user_id'] for user_group in user_groups ]
            if len(user_ids) == 0:  return []
            return self.user.find_by_ids(user_ids)

        if not params:
            # in case there is no params
            users = self.user.find({})
        else:
            # for other parameters
            users = self.user.find(params)
        if current_user['level'] == self.USER_LEVEL_ADMIN:
            return users
        # return only the users who are in the same group with the current user among the returned users
        user_groups = self.user_group_controller.find(access_token, {'user_id': current_user['id']})
        group_ids = [ user_group['group_id'] for user_group in user_groups]
        user_groups = self.user_group_controller.find(access_token, {'group_ids': group_ids})
        user_ids = [ user_group['user_id'] for user_group in user_groups]
        return [ user for user in users if user['id'] in user_ids]
