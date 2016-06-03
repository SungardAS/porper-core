
from dynamodb import Dynamodb

class AccessToken(Dynamodb):

    def __init__(self, region):
        Dynamodb.__init__(self, region)
        self.table_name = "tokens"

    def create(self, params):
        item = {
            "access_token": {"S": params['access_token']},
            "refresh_token": {"S": params['refresh_token']},
            "refreshed_time": {"S": params['refreshed_time']},
            "user_id": {"S": params['user_id']}
        };
        return self.save(item)

    def update(self, params):
        if not params.get('refresh_token') or not params.get('userid'):
            items = self.find(params)
            if len(items) == 0:
                raise Exception("access_token [%s] not exist" % params['access_token'])
            params['refresh_token'] = items[0]['refresh_token']
            params['user_id'] = items[0]['user_id']
        item = {
            "access_token": {"S": params['access_token']},
            "refresh_token": {"S": params['refresh_token']},
            "refreshed_time": {"S": params['refreshed_time']},
            "user_id": {"S": params['user_id']}
        };
        return self.save(item)

    def find(self, params):
        return Dynamodb.find(self,
            KeyConditionExpression="access_token = :access_token",
            ExpressionAttributeValues={ ":access_token": {"S": params['access_token']} }
        )
