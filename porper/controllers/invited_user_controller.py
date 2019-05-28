
from datetime import datetime
from porper.controllers.meta_resource_controller import MetaResourceController

from porper.controllers.meta_resource_controller import ADMIN_GROUP_ID

class InvitedUserController(MetaResourceController):

    def __init__(self, connection):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.invited_user import InvitedUser
        self.invited_user = InvitedUser(connection)
        #from porper.models.user_group import UserGroup
        #self.user_group = UserGroup(connection)
        #from porper.controllers.token_controller import TokenController
        #self.token_controller = TokenController(connection)
        #from porper.controllers.permission_controller import PermissionController
        #self.permission_controller = PermissionController(self.connection)
        from porper.controllers.user_group_controller import UserGroupController
        self.user_group_controller = UserGroupController(self.connection)


    def create(self, access_token, params):
        """
        possible attributes in params
            - auth_type, email, group_id, [invited_at, invited_by, is_admin]
        """
        group_id = params['group_id']
        current_user = self.find_user_level(access_token, group_id)
        if current_user['level'] != self.USER_LEVEL_ADMIN and current_user['level'] != self.USER_LEVEL_GROUP_ADMIN:
            raise Exception("not permitted")
        items = self.invited_user.find({'email': params['email'], 'auth_type': params['auth_type']})
        if items and items[0]['state'] == self.invited_user.REGISTERED:
            raise Exception("Already registered")
        return self._save(current_user['id'], params)


    def _save(self, user_id, params):
        invited_users = self.invited_user.find(params)
        if len(invited_users) > 0:
            print('already invited')
            return True
        if not params.get('invited_by'):
            params['invited_by'] = user_id
        if not params.get('invited_at'):
            params['invited_at'] = str(datetime.utcnow())
        if not params.get('state'):
            params['state'] = self.invited_user.INVITED
        if not params.get('is_admin'):
            params['is_admin'] = False
        else:
            params['is_admin'] = True
        return self.invited_user.create(params)


    def update(self, access_token, params):
        """
        attributes in params
            - auth_type, email
        """
        items = self.invited_user.find({'email': params['email'], 'auth_type': params['auth_type']})
        if not items:
            raise Exception("not invited")
        if items[0]['state'] == self.invited_user.REGISTERED:
            raise Exception("Already registered")
        group_id = items[0]['group_id']
        current_user = self.find_user_level(access_token, group_id)
        if current_user['level'] != self.USER_LEVEL_ADMIN and current_user['level'] != self.USER_LEVEL_GROUP_ADMIN:
            raise Exception("not permitted")
        params['state'] = self.invited_user.INVITED
        return self.invited_user.update(params)


    def find(self, access_token, params):
        """
        possible attributes in params
            - group_id
            - auth_type, email
            - None
        """

        group_id = params.get('group_id')
        current_user = self.find_user_level(access_token, group_id)

        if group_id:
            if current_user['level'] != self.USER_LEVEL_ADMIN and current_user['level'] != self.USER_LEVEL_GROUP_ADMIN:
                raise Exception("not permitted")
            return self.invited_user.find({'group_id': group_id})

        if params:

            invited_users = self.invited_user.find(params)

            # if the current user is admin, return all fetched invited_users
            if current_user['level'] == self.USER_LEVEL_ADMIN:
                return invited_users

            # return only invited users who belong to groups where the current user is a group admin
            user_groups = self.user_group_controller.find(access_token, {'user_id': current_user['id']})
            group_ids = [ user_group['group_id'] for user_group in user_groups if user_group['is_admin'] ]
            allowed_invited_users = [ invited_user for invited_user in invited_users if invited_user['group_id'] in group_ids ]
            return allowed_invited_users

        else:

            # if the current user is admin, return all invited_users
            if current_user['level'] == self.USER_LEVEL_ADMIN:
                return self.invited_user.find({})

            # return all invited users of groups where the current user is a group admin
            user_groups = self.user_group_controller.find(access_token, {'user_id': current_user['id']})
            group_ids = [ user_group['group_id'] for user_group in user_groups if user_group['is_admin'] ]
            if len(group_ids) > 0:
                params['group_ids'] = group_ids
                return self.invited_user.find(params)

        return []


    def delete(self, access_token, params):
        """
        attributes in params
            - auth_type, email
        """
        items = self.invited_user.find({'email': params['email'], 'auth_type': params['auth_type']})
        if not items:
            raise Exception("not invited")
        removeuser=params.get('removeuser')    
        if removeuser=="Y":
           print("Skip registered check") 
        else:
            if items[0]['state'] == self.invited_user.REGISTERED:
                raise Exception("Already registered")
        group_id = items[0]['group_id']
        current_user = self.find_user_level(access_token, group_id)
        if current_user['level'] != self.USER_LEVEL_ADMIN and current_user['level'] != self.USER_LEVEL_GROUP_ADMIN:
            raise Exception("not permitted")
        params['state'] = self.invited_user.CANCELLED
        self.invited_user.update(params)
        return True
