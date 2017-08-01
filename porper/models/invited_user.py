
from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from decimal_encoder import DecimalEncoder

class InvitedUser:

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.table = dynamodb.Table('invited_users')
        self.INVITED = 'invited'
        self.REGISTERED = 'registered'

    def create(self, params):
        try:
            response = self.table.put_item(
               Item=params
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise
        else:
            print("PutItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))
            return params['email']

    def update(self, params):
        try:
            response = self.table.update_item(
                Key={
                    'email': params["email"]
                },
                UpdateExpression="set #state = :state",
                ExpressionAttributeNames={
                    '#state': 'state'
                },
                ExpressionAttributeValues={
                    ':state': params['state']
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise
        else:
            print("UpdateItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def _fill_related_attrs(self, items):
        if len(items) == 0: return []
        from user import User
        user = User(self.dynamodb)
        user_items = user.find({'ids': [item['invited_by'] for item in items]})
        from role import Role
        role = Role(self.dynamodb)
        role_items = role.find({'ids': [item['role_id'] for item in items]})
        if len(user_items) == 0 or len(role_items) == 0:    return []
        for item in items:
            item['invited_by_email'] = [user_item['email'] for user_item in user_items if user_item['id'] == item['invited_by']][0]
            item['role_name'] = [role_item['name'] for role_item in role_items if role_item['id'] == item['role_id']][0]
        return items

    def find(self, params):

        if params.get('email'):
            response = self.table.get_item(
                Key={
                    'email': params['email']
                }
            )
            if response.get('Item'):
                item = response['Item']
                print("GetItem succeeded:")
                print(json.dumps(item, indent=4, cls=DecimalEncoder))
                return self._fill_related_attrs([item])
            else:
                print("GetItem returns no item:")
                return []

        if params.get('role_id'):
            response = self.table.scan(
                FilterExpression="role_id = :role_id",
                ExpressionAttributeValues={":role_id": params['role_id']}
            )
            for i in response['Items']:
                print(json.dumps(i, cls=DecimalEncoder))
            return self._fill_related_attrs(response["Items"])

        if params.get('role_ids'):
            eav = {}
            fe = 'role_id in ('
            for index, role_id in enumerate(params['role_ids']):
                role_id_name = ':role_id_%s' % index
                if index == 0:
                    fe += role_id_name
                else:
                    fe += ', ' + role_id_name
                eav[role_id_name] = role_id
            fe += ')'
            print(fe)
            print(eav)
            response = self.table.scan(
                FilterExpression=fe,
                ExpressionAttributeValues=eav
            )
            for i in response['Items']:
                print(json.dumps(i, cls=DecimalEncoder))
            return self._fill_related_attrs(response["Items"])

        return []
