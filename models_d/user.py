
from dynamodb import Dynamodb

class User(Dynamodb):

    def __init__(self, region):
        Dynamodb.__init__(self, region)
        self.table_name = "users"

    def create(self, params):
        item = {
            "id": {"S": params['id']},
            "email": {"S": params['email']},
            "family_name": {"S": params['family_name']},
            "given_name": {"S": params['given_name']},
            "name": {"S": "%s %s" % (params['given_name'], params['family_name'])}
        };
        return self.save(item)

    def find(self, params):
        if params.get('ids') == [] or params.get('role_ids') == []:
            return []
        if params.get('role_id') or params.get('role_ids'):
            user_ids = self.find_user_role(params)
            print user_ids
            keys = [ { "id": {"S": id} } for id in user_ids]
            return self.find_batch(
                RequestItems = {
                    self.table_name: {
                        'Keys': keys
                    }
                }
            )
        if params.get('id'):
            return Dynamodb.find(self,
                KeyConditionExpression="id = :id",
                ExpressionAttributeValues={ ":id": {"S": params['id']} }
            )
        if params.get('ids'):
            keys = [ { "id": {"S": id} } for id in params.get('ids')]
            return self.find_batch(
                RequestItems = {
                    self.table_name: {
                        'Keys': keys
                    }
                }
            )
        return self.find_all()

    def find_user_role(self, params):
        from user_role import UserRole
        user_role = UserRole(self.region)
        user_roles = user_role.find(params)
        res = [user_role['user_id'] for user_role in user_roles]
        # remove duplicates before returning data
        return list(set(res))
