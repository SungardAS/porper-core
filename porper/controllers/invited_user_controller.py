
from datetime import datetime
from porper.controllers.meta_resource_controller import MetaResourceController

class InvitedUserController(MetaResourceController):

    def __init__(self, connection=None):
        MetaResourceController.__init__(self, connection)
        from porper.models.invited_user import InvitedUser
        self.invited_user = InvitedUser(self.connection)
        from porper.models.user_group import UserGroup
        self.user_group = UserGroup(self.connection)
        # from porper.controllers.user_group_controller import UserGroupController
        # self.user_group_controller = UserGroupController(self.connection)

        self.permission_name = "invite"


    def create(self, access_token, params):
        """
        possible attributes in params
            - auth_type, email, group_id, [invited_at, invited_by, is_admin]
        """
        self.find_user_level(access_token)

        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        if not self.is_member(group_id=params['group_id']):
            raise Exception("not permitted")

        search_params = {'email': params['email'], 'auth_type': params['auth_type']}
        items = self.invited_user.find(search_params)
        if items:
            if items[0]['state'] == self.invited_user.REGISTERED:
                raise Exception("Already registered")
            if items[0]['state'] == self.invited_user.INVITED:
                print("Already invited")
                return True

        return self._save(self.user_id, params)


    def _save(self, user_id, params):
        # invited_users = self.invited_user.find(params)
        # if len(invited_users) > 0:
        #     print('already invited')
        #     return True
        if not params.get('invited_by'):
            params['invited_by'] = user_id
        if not params.get('invited_at'):
            params['invited_at'] = str(datetime.utcnow())
        if not params.get('state'):
            params['state'] = self.invited_user.INVITED
        # if not params.get('is_admin'):
        #     params['is_admin'] = False
        # else:
        #     params['is_admin'] = True
        return self.invited_user.create(params)


    def update(self, access_token, params):
        """
        attributes in params
            - auth_type, email
        """
        self.find_user_level(access_token)

        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        items = self.invited_user.find({'email': params['email'], 'auth_type': params['auth_type']})
        if not items or not self.is_member(group_id=items[0]['group_id']):
            raise Exception("not permitted")

        if items[0]['state'] == self.invited_user.REGISTERED:
            raise Exception("Already registered")

        return self.invited_user.update_state(params['email'], params['auth_type'], params['state'])


    def find(self, access_token, params):
        """
        possible attributes in params
            - group_id
            - auth_type, email
            - None
        """

        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_read):
            raise Exception("not permitted")

        # if the current user is admin, return all fetched invited_users
        if self.is_admin:
            return self.invited_user.find(params)
        elif self.is_customer_admin:
            return self.invited_user.find(params, customer_id=current_user.customer_id)
        else:
            return self.invited_user.find(params, user_id=current_user.user_id)


    def delete(self, access_token, params):
        """
        attributes in params
            - auth_type, email
        """
        self.find_user_level(access_token)

        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        items = self.invited_user.find({'email': params['email'], 'auth_type': params['auth_type']})
        if not items or not self.is_member(group_id=items[0]['group_id']):
            raise Exception("not permitted")

        if items[0]['state'] == self.invited_user.REGISTERED:
            raise Exception("Already registered")

        params['state'] = self.invited_user.CANCELLED
        self.invited_user.update_state(params['email'], params['auth_type'], params['state'])
        return True
