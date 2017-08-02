
import sys
sys.path.append('../../porper')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)

#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647'   # alex.ough's token
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'    # cloud_test_user's token
print group_controller.find_all(access_token)

connection.commit()
