
import uuid
from dynamodb import Dynamodb

class UserRole(Dynamodb):

    def __init__(self, region):
        Dynamodb.__init__(self, region)
        self.table_name = "users_roles"
        self.secondary_index_name = "role_id-id-index"

    def create(self, params):
        item = {
            "id": {"S": str(uuid.uuid4())},
            "user_id": {"S": params['user_id']},
            "role_id": {"S": params['role_id']},
            "is_admin": {"BOOL": params['is_admin']}
        };
        return self.save(item)

    def find(self, params):

        if params.get('user_id') and params.get('role_id'):
            return Dynamodb.find(self,
                KeyConditionExpression="user_id = :user_id",
                FilterExpression="role_id = :role_id",
                ExpressionAttributeValues={ ":user_id": {"S": params['user_id']}, ":role_id": {"S": params['role_id']} },
            )

        if params.get('user_id'):
            return Dynamodb.find(self,
                KeyConditionExpression="user_id = :user_id",
                ExpressionAttributeValues={ ":user_id": {"S": params['user_id']} }
            )

        if params.get('role_id'):
            return Dynamodb.find(self,
                KeyConditionExpression="role_id = :role_id",
                ExpressionAttributeValues={ ":role_id": {"S": params['role_id']} },
                IndexName=self.secondary_index_name
            )

        if params.get('role_ids'):
            role_ids = params['role_ids']
            """
            # we need to multiple queries for each role_id
            # because it says "Invalid operator used in KeyConditionExpression: OR"
            user_roles = []
            for role_id in role_ids:
                res = Dynamodb.find(self,
                    KeyConditionExpression="role_id = :role_id",
                    ExpressionAttributeValues={":role_id": {"S": role_id}},
                    IndexName=self.secondary_index_name
                )
                print res
                user_roles = user_roles + res
            return user_roles
            """
            # or we can call just one scan
            filter_expression = []
            expression_attributes = {}
            for i in range(0, len(role_ids)):
                filter_expression.append("role_id = :role_id_%s" % i)
                expression_attributes[":role_id_%s" % i] = {"S": role_ids[i]}
            filter_expression_str = " OR ".join(filter_expression)
            print 'roles - FilterExpression : %s' % filter_expression_str
            print 'roles - ExpressionAttributeValues : %s' % expression_attributes
            return self.find_all(
                FilterExpression=filter_expression_str,
                ExpressionAttributeValues=expression_attributes
            )

        return []
