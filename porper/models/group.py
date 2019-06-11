
from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
#from decimal_encoder import DecimalEncoder
from porper.models.resource import Resource

import os
import uuid
import aws_lambda_logging
import logging

logger = logging.getLogger()
loglevel = "INFO"
logging.basicConfig(level=logging.ERROR)
aws_lambda_logging.setup(level=loglevel)

class Group(Resource):

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.table = dynamodb.Table(os.environ.get('GROUP_TABLE_NAME'))

    def create(self, params, paths=None):
        if not params.get('id'):
            params['id'] = str(uuid.uuid4())
        return Resource.create(self, params)


    def is_admin_group(self, group):
        from porper.models.role import Role
        self.role = Role(self.dynamodb)
        from porper.models.function import Function
        self.function = Function(self.dynamodb)
        admin_permission = {'resource': 'admin', 'action': 'w'}
        if group.get('role_id'):
            role = self.role.find_by_id(group['role_id'])
            for function in self.function.find_by_ids(role['functions']):
                for permission in function['permissions']:
                    if permission['resource'] == admin_permission['resource'] and permission['action'] == admin_permission['action']:
                        return True
        return False


    def find_admin_groups(self):
        admin_groups = []
        for group in self.find({}):
            if self.is_admin_group(group):
                admin_groups.append(group)
        return admin_groups

    """def _find_by_ids(self, ids):
        eav = {}
        fe = 'id in ('
        for index, id in enumerate(ids):
            id_name = ':id_%s' % index
            if index == 0:
                fe += id_name
            else:
                fe += ', ' + id_name
            eav[id_name] = id
        fe += ')'
        print(fe)
        print(eav)
        return self.table.scan(
            FilterExpression=fe,
            ExpressionAttributeValues=eav
        )['Items']


    def find(self, params):

        if not params:
            return self.table.scan()['Items']

        if params.get('id'):
            response = self.table.get_item(
                Key={
                    'id': params['id']
                }
            )
            if response.get('Item'):
                item = response['Item']
                print("GetItem succeeded:")
                print(json.dumps(item, indent=4, cls=DecimalEncoder))
                return [item]
            else:
                print("GetItem returns no item:")
                return []

        if params.get('ids'):
            return self._find_by_ids(params['ids'])

        return []"""
