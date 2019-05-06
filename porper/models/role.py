
from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from porper.models.decimal_encoder import DecimalEncoder
from porper.models.resource import Resource

import os
import uuid

class Role(Resource):

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.table = dynamodb.Table(os.environ.get('ROLE_TABLE_NAME'))

    def create(self, params):
        if not params.get('id'):
            params['id'] = str(uuid.uuid4())
        return Resource.create(self, params)
