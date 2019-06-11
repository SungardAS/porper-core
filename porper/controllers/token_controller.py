
from datetime import datetime

class TokenController:

    def __init__(self, connection):
        self.connection = connection
        from porper.models.access_token import AccessToken
        self.access_token = AccessToken(connection)
        from porper.models.user_group import UserGroup
        self.user_group = UserGroup(connection)

    def find_user_id(self, access_token):
        params = {
            'access_token': access_token
        }
        return self.access_token.find(params)[0]['user_id']

    def is_admin(self, user_id):
        from porper.controllers.meta_resource_controller import ADMIN_GROUP_ID
        row = self.user_group.find({'user_id': user_id, 'group_id': ADMIN_GROUP_ID})
        if len(row) > 0:  return True
        else: return False

    def create(self, access_token, params):
        return self.save(params['access_token'], params['refresh_token'], params['user_id'])

    def save(self, access_token, refresh_token, user_id):
        params = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'refreshed_time': str(datetime.utcnow())
        }
        if user_id: params['user_id'] = user_id
        rows = self.access_token.find(params)
        if len(rows) == 0:
            print('saving tokens : {}'.format(params))
            return self.access_token.create(params)
        else:
            print('updating token : {}'.format(params))
            return self.access_token.update(params)

    def find(self, access_token, params):
        # is_admin_user = False
        # user_id = self.find_user_id(access_token)
        # if user_id:
        #     is_admin_user = self.is_admin(user_id)
        # if not is_admin_user:
        #     params = {'access_token': access_token}
        rows = self.access_token.find(params)
        if len(rows) == 0:
            raise Exception("unauthorized")
        return rows

    def delete(self, access_token, params):
        return self.access_token.delete(access_token)
