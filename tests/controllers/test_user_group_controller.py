
import sys
sys.path.append('../../porper')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

from porper.controllers.user_group_controller import UserGroupController
user_group_controller = UserGroupController(dynamodb)

user_id = 'b2fc88a6-7253-4850-8d5a-07639b1315aa'
print user_group_controller.find(None, {'user_id': user_id})
group_id = '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a'
print user_group_controller.find(None, {'group_id': group_id})

connection.commit()
