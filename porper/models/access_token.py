
from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from decimal_encoder import DecimalEncoder

import dateutil.parser

class AccessToken:

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.table = dynamodb.Table('access_tokens')

    def create(self, params):
        try:
            params["time_stamp"] = dateutil.parser.parse(params['refreshed_time']).strftime("%s")   # will be used as TTL attribute
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
        try:
            response = self.table.update_item(
                Key={
                    'access_token': params["access_token"]
                },
                UpdateExpression="set refresh_token = :rtoken, refreshed_time=:rtime, time_stamp=:ts",
                ExpressionAttributeValues={
                    ':rtoken': params['refresh_token'],
                    ':rtime': params['refreshed_time'],
                    ':ts': dateutil.parser.parse(params['refreshed_time']).strftime("%s")
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise
        else:
            print("UpdateItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def find(self, params):
        response = self.table.get_item(
            Key={
                'access_token': params["access_token"]
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
