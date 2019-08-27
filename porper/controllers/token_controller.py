
from porper.controllers.meta_resource_controller import MetaResourceController
from datetime import datetime

class TokenController(MetaResourceController):

    def __init__(self, connection=None):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.access_token import AccessToken
        self.access_token = AccessToken(self.connection)

        self.permission_name = 'Token'


    def find(self, access_token, params):
        return self.access_token.find(access_token)


    # def find_user_id(self, access_token):
    #     params = {
    #         'access_token': access_token
    #     }
    #     return self.access_token.find(params)[0]['user_id']


    # def create(self, access_token, params):
    #     return self.save(params['access_token'], params['refresh_token'], params['user_id'])
    #
    #
    # def save(self, access_token, refresh_token, user_id):
    #     params = {
    #         'access_token': access_token,
    #         'refresh_token': refresh_token,
    #         'refreshed_time': str(datetime.utcnow())
    #     }
    #     if user_id: params['user_id'] = user_id
    #     rows = self.access_token.find(params)
    #     if len(rows) == 0:
    #         print('saving tokens : {}'.format(params))
    #         return self.access_token.create(params)
    #     else:
    #         print('updating token : {}'.format(params))
    #         return self.access_token.update(params)


    # def find(self, access_token, params):
    #     current_user = self.find_user_level(access_token)
    #     # is_admin_user = False
    #     # user_id = self.find_user_id(access_token)
    #     # if user_id:
    #     #     is_admin_user = self.is_admin(user_id)
    #     # if not is_admin_user:
    #     #     params = {'access_token': access_token}
    #     rows = self.access_token.find(params)
    #     if len(rows) == 0:
    #         raise Exception("unauthorized")
    #     return rows
    #
    #
    # def delete(self, access_token, params):
    #     return self.access_token.delete(access_token)
