
import sys
sys.path.insert(0, r'..')
from datetime import datetime

class AccessTokenController:

    def __init__(self, region, connection):
        self.region = region
        self.connection = connection

        if connection:
            from models.token import Token
            self.token = Token(connection)
        else:
            from models_d.token import Token
            self.token = Token(region)

    def create(self, access_token, params):
        return self.save(params['access_token'], params['refresh_token'], params['user_id'])

    def save(self, access_token, refresh_token, user_id):
        params = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'refreshed_time': str(datetime.utcnow())
        }
        if user_id: params['user_id'] = user_id
        rows = self.token.find(params)
        if len(rows) == 0:
            print 'saving tokens : %s' % params
            return self.token.create(params)
        else:
            print 'updating token : %s' % params
            return self.token.update(params)

    def find(self, access_token):
        params = {
            'access_token': access_token
        }
        rows = self.token.find(params)
        if len(rows) == 0:
            raise Exception("unauthorized")
        return rows
