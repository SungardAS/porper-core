
from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from decimal_encoder import DecimalEncoder

class Resource:

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.table = None

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
            return params['access_token']

    def update(self, params):
        if params.get('id') is None:
            raise Exception("no id is given in update")
        ue = "set "
        eav = {}
        for index, key in params.keys():
            if index > 0:
                ue += ', '
            if key != 'id':
                ue += "%s = :%s" % (key, key)
                eav[':%s' % key] = params[key]
        try:
            response = self.table.update_item(
                Key={
                    'id': params["id"]
                },
                UpdateExpression=ue,
                ExpressionAttributeValues=eav,
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise
        else:
            print("UpdateItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def find_by_id(self, id):
        response = self.table.get_item(
            Key={
                'id': id
            }
        )
        if response.get('Item'):
            item = response['Item']
            print("GetItem succeeded:")
            print(json.dumps(item, indent=4, cls=DecimalEncoder))
            return item
        else:
            print("GetItem returns no item:")
            return None

    def find_by_ids(self, ids):
        eav = {}
        fe = 'id in ('
        for index, item in enumerate(items):
            id_name = ':id_%s' % index
            if index == 0:
                fe += id_name
            else:
                fe += ', ' + id_name
            eav[id_name] = item['id']
        fe += ')'
        print(fe)
        print(eav)
        return self.table.scan(
            FilterExpression=fe,
            ExpressionAttributeValues=eav
        )['Items']

    def find(self, params):
        raise Exception("Not implemented")

    def delete(self, id):
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
