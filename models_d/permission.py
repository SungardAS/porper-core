
import uuid
from dynamodb import Dynamodb

class Permission(Dynamodb):

    def __init__(self, region):
        Dynamodb.__init__(self, region)
        self.table_name = "permissions"
        self.null_id = '0'

    def create(self, params):
        item = {
            "id": {"S": str(uuid.uuid4())},
            "resource": {"S": params['resource']},
            "action": {"S": params['action']},
            "value": {"S": params['value']}
        };
        if params.get('user_id'):
            item['user_id'] = {"S": params['user_id']};
            item['role_id'] = {"S": self.null_id};
        if params.get('role_id'):
            item['role_id'] = {"S": params['role_id']};
            item['user_id'] = {"S": self.null_id};
        if (params.get('condition')):
            item['condition'] = {"S": params['condition']};
        return self.save(item);

    def delete(self, params):
        if params.get('id') and params.get('user_id'):
            key = {"id": {"S": params['id']}, "user_id": {"S": params['user_id']}}
            return self.remove(Key=key)
        items = self.find(params)
        if len(items) == 0:
            raise Exception("premission [%s:%s] not exist" % (params['user_id'], params('role_id')))
        key = {"id": {"S": items[0]['id']}, "user_id": {"S": items[0]['user_id']}}
        return self.remove(Key=key)

    def find(self, params):

        key_condition = None
        filter_expression = []
        expression_names = {}
        expression_attributes = {}
        index_name = None

        if params.get('resource'):
            filter_expression.append("#resource = :resource")
            expression_names["#resource"] = "resource"
            expression_attributes[":resource"] = {"S": params['resource']}
        if params.get('action'):
            filter_expression.append("#action = :action")
            expression_names["#action"] = "action"
            expression_attributes[":action"] = {"S": params['action']}
        if params.get('value'):
            filter_expression.append("(#value = :value OR #value = :all)")
            expression_names["#value"] = "value"
            expression_attributes[":value"] = {"S": params['value']}
            expression_attributes[":all"] = {"S": "*"}
        if params.get('user_id'):
            key_condition = "user_id = :user_id"
            expression_attributes[":user_id"] = {"S": params['user_id']}
        elif params.get('role_id'):
            key_condition = "role_id = :role_id"
            expression_attributes[":role_id"] = {"S": params['role_id']}
            index_name = "role_id-id-index"
        filter_express_str = " AND ".join(filter_expression)

        print 'KeyConditionExpression : %s' % key_condition
        print 'ExpressionAttributeValues : %s' % expression_attributes
        kwargs = {
            'KeyConditionExpression': key_condition,
            'ExpressionAttributeValues': expression_attributes
        }
        if filter_expression:
            print 'FilterExpression : %s' % filter_express_str
            kwargs['FilterExpression'] = filter_express_str
        if expression_names:
            print 'ExpressionAttributeNames : %s' % expression_names
            kwargs['ExpressionAttributeNames'] = expression_names
        if index_name:
            print 'IndexName : %s ' % index_name
            kwargs['IndexName'] = index_name
        res = Dynamodb.find(self, **kwargs)

        if params.get('user_id') and params.get('all'):
            # we need to find permissions of all roles where this given user belongs
            # and merge them to the permissions of the given user
            # we cannot make these 2 queries into one because the primary index (user_id) value is different
            #   to find permissions of the given user : user_id
            #   to find permissions of all roles : self.null_id
            # TODO : This needs to be enhanced if we find better solution!!!!
            role_res = self.find_role_permissions(params)
        else:
            role_res = []

        return res + role_res

    def find_user_role(self, user_id):
        from user_role import UserRole
        user_role = UserRole(self.region)
        params = {'user_id': user_id}
        user_roles = user_role.find(params)
        return [user_role['role_id'] for user_role in user_roles]

    def build_role_filter_expression(self, role_ids):
        filter_expression = []
        expression_attributes = {}
        for i in range(0, len(role_ids)):
            filter_expression.append("role_id = :role_id_%s" % i)
            expression_attributes[":role_id_%s" % i] = {"S": role_ids[i]}
        filter_expression_str = " OR ".join(filter_expression)
        print 'roles - FilterExpression : %s' % filter_expression_str
        print 'roles - ExpressionAttributeValues : %s' % expression_attributes

        return {'filter_expression_str': filter_expression_str, 'expression_attributes': expression_attributes}

    def find_role_permissions(self, params):
        key_condition = None
        filter_expression = []
        expression_names = {}
        expression_attributes = {}
        index_name = None

        key_condition = "user_id = :user_id"
        expression_attributes[":user_id"] = {"S": self.null_id}

        if params.get('resource'):
            filter_expression.append("#resource = :resource")
            expression_names["#resource"] = "resource"
            expression_attributes[":resource"] = {"S": params['resource']}
        if params.get('action'):
            filter_expression.append("#action = :action")
            expression_names["#action"] = "action"
            expression_attributes[":action"] = {"S": params['action']}
        if params.get('value'):
            filter_expression.append("(#value = :value OR #value = :all)")
            expression_names["#value"] = "value"
            expression_attributes[":value"] = {"S": params['value']}
            expression_attributes[":all"] = {"S": "*"}

        role_ids = self.find_user_role(params['user_id'])
        role_id_params = self.build_role_filter_expression(role_ids)
        if filter_expression:
            filter_express_str = " AND ".join(filter_expression) + " AND (" + role_id_params['filter_expression_str'] + ")"
        else:
            filter_express_str = role_id_params['filter_expression_str']
        for key in role_id_params['expression_attributes'].keys():
            expression_attributes[key] = role_id_params['expression_attributes'][key]

        print 'MultiRoles - KeyConditionExpression : %s' % key_condition
        print 'MultiRoles - ExpressionAttributeValues : %s' % expression_attributes
        kwargs = {
            'KeyConditionExpression': key_condition,
            'ExpressionAttributeValues': expression_attributes
        }
        if filter_express_str:
            print 'MultiRoles - FilterExpression : %s' % filter_express_str
            kwargs['FilterExpression'] = filter_express_str
        if expression_names:
            print 'MultiRoles - ExpressionAttributeNames : %s' % expression_names
            kwargs['ExpressionAttributeNames'] = expression_names
        return Dynamodb.find(self, **kwargs)
