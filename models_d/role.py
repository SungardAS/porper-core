
import uuid
from dynamodb import Dynamodb

class Role(Dynamodb):

    def __init__(self, region):
        Dynamodb.__init__(self, region)
        self.table_name = "roles"

    def create(self, params):
        if not params.get('id'):
            params['id'] = str(uuid.uuid4())
        item = {
            "id": {"S": params['id']},
            "name": {"S": params['name']}
        };
        return self.save(item)

    def find(self, params):
        if params.get('ids') == []:
            return []
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
