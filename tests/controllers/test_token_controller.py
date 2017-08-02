
import sys
sys.path.append('../../porper')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

from porper.controllers.token_controller import TokenController
token_controller = TokenController(dynamodb)

user_id = 'b2fc88a6-7253-4850-8d5a-07639b1315aa'
print token_controller.save('access1', 'refresh1', user_id)
print token_controller.find('access1')

connection.commit()
