
from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from decimal_encoder import DecimalEncoder

import uuid

class Permission:

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.table = dynamodb.Table('permissions')

    def create(self, params):
        if not params.get('id'):
            params['id'] = str(uuid.uuid4())
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

    def _find_id(self, params):
        if params.get('user_id') is None and params.get('role_id') is None:
            return None
        fe = "action = :action and resource = :resource and #value = :value"
        ean = {'#value': 'value'}
        eav = {':action': params['action'], ':resource': params['resource'], ':value': params['value']}
        if params.get('user_id'):
            fe += " and user_id = :user_id"
            eav[':user_id'] = params['user_id']
        elif params.get('role_id'):
            fe += " and role_id = :role_id"
            eav[':role_id'] = params['role_id']
        response = self.table.scan(
            FilterExpression=fe,
            ExpressionAttributeNames=ean,
            ExpressionAttributeValues=eav
        )
        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))
        if len(response["Items"]) == 0: return None
        else:   return response["Items"][0]['id']

    def delete(self, params):
        id = params.get('id')
        if id is None:
            id = self._find_id(params)
        if id is None:
            print("No item found to delete")
            return
        try:
            response = self.table.delete_item(
                Key={
                    'id': id
                },
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise
        else:
            print("DeleteItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))
            return

    def find(self, params):

        if not params:
            return self.table.scan()['Items']

        fe = ""
        ean = {}
        eav = {}
        if params.get('resource'):
            if fe != "":
                fe += " and "
            fe += "#resource = :resource"
            eav[':resource'] = params['resource']
            ean['#resource'] = 'resource'
        if params.get('action'):
            if fe != "":
                fe += " and "
            fe += "#action = :action"
            eav[':action'] = params['action']
            ean['#action'] = 'action'
        if params.get('value'):
            if fe != "":
                fe += " and "
            fe += "#value in (:value1, :value2)"
            eav[':value1'] = params['value']
            eav[':value2'] = '*'
            ean['#value'] = 'value'
        if params.get('user_id'):
            if params.get('all'):
                from user_role import UserRole
                user_role = UserRole(self.dynamodb)
                user_role_items = user_role.find({'user_id': params['user_id']})
                role_ids = [ user_role_item['role_id'] for user_role_item in user_role_items ]
                if fe != "":
                    fe += " and "
                fe += "(#user_id = :user_id or role_id in ("
                for index, role_id in enumerate(role_ids):
                    role_id_name = ':role_id_%s' % index
                    if index == 0:
                        fe += role_id_name
                    else:
                        fe += ', ' + role_id_name
                    eav[role_id_name] = role_id
                eav[':user_id'] = params['user_id']
                fe += '))'
                print(fe)
                print(eav)
            else:
                if fe != "":
                    fe += " and "
                fe += "#user_id = :user_id"
                eav[':user_id'] = params['user_id']
            ean['#user_id'] = 'user_id'
        elif params.get('role_id'):
            if fe != "":
                fe += " and "
            fe += "#role_id = :role_id"
            eav[':role_id'] = params['role_id']
            ean['#role_id'] = 'role_id'
        print(fe)
        print(ean)
        print(eav)
        response = self.table.scan(
            FilterExpression=fe,
            ExpressionAttributeNames=ean,
            ExpressionAttributeValues=eav
        )
        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))
        return response["Items"]
