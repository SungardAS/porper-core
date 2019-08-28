
from datetime import datetime
from porper.controllers.meta_resource_controller import MetaResourceController

class InvitedUserController(MetaResourceController):

    def __init__(self, connection=None):
        MetaResourceController.__init__(self, connection)
        from porper.models.invited_user import InvitedUser
        self.invited_user = InvitedUser(self.connection)
        from porper.models.user_group import UserGroup
        self.user_group = UserGroup(self.connection)
        from porper.models.group import Group
        self.group = Group(self.connection)
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
        customer_id = None
        if 'customer_id' in params:
            customer_id = params['customer_id']
            del params['customer_id']
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
        params = self.invited_user.create(params)
        if customer_id:
            params['customer_id'] = customer_id
        return params


    def update(self, access_token, params):
        """
        attributes in params
            - auth_type, email
        """
        self.find_user_level(access_token)

        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        items = self.invited_user.find_simple({'email': params['email'], 'auth_type': params['auth_type']})
        if not items:
            raise Exception("not permitted")

        if items[0]['state'] == self.invited_user.REGISTERED:
            raise Exception("Already registered")

        ret = self.group.find_by_id(items[0]['group_id'])
        if not ret:
            raise Exception("not permitted")

        if self.is_customer_admin:
            if self.customer_id != ret['customer_id']:
                raise Exception("not permitted")
        elif not self.is_admin:
            if not self.is_member(group_id=items[0]['group_id']):
                raise Exception("not permitted")

        params['state'] = self.invited_user.INVITED
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
            return self.invited_user.find(params, customer_id=self.customer_id)
        else:
            return self.invited_user.find(params, user_id=self.user_id)


    def delete(self, access_token, params):
        """
        attributes in params
            - auth_type, email
        """
        self.find_user_level(access_token)

        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        items = self.invited_user.find_simple({'email': params['email'], 'auth_type': params['auth_type']})
        if not items:
            raise Exception("not permitted")

        if items[0]['state'] == self.invited_user.REGISTERED:
            raise Exception("Already registered")

        ret = self.group.find_by_id(items[0]['group_id'])
        if not ret:
            raise Exception("not permitted")

        if self.is_customer_admin:
            if self.customer_id != ret['customer_id']:
                raise Exception("not permitted")
        elif not self.is_admin:
            if not self.is_member(group_id=items[0]['group_id']):
                raise Exception("not permitted")

        params['state'] = self.invited_user.CANCELLED
        self.invited_user.update_state(params['email'], params['auth_type'], params['state'])
        return True
