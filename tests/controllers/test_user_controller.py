
import sys
sys.path.append('../../porper')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

from porper.controllers.user_controller import UserController
user_controller = UserController(dynamodb)

#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647';  # alex.ough
#access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5';    # cloud_test_user
#params = {};
#group_id = '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a';   # public
group_id = '3867c370-552f-43b8-bed9-6aa00ffc41b4';   # Awesome Group
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5';    # cloud_test_user
params = {'group_id': group_id};
print user_controller.find_all(access_token, params)

connection.commit()
