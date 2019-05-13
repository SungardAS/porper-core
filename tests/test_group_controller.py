
import sys
sys.path.append("..")

import os
import boto3
region = os.environ.get('AWS_DEFAULT_REGION')
dynamodb = boto3.resource('dynamodb',region_name=region)

#########################################################################################################
# Preparation
# Find the access_token of an admin
#########################################################################################################
from util import find_admin_token
admin_access_token = find_admin_token()


### Create a group
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)

customer_id = '64b3bbf4-1f3d-446f-b697-06c2a68f2053'
group_obj = {'name': 'group_1', 'customer_id': customer_id}
ret = group_controller.create(admin_access_token, group_obj)
# {'name': 'group_1', 'customer_id': '64b3bbf4-1f3d-446f-b697-06c2a68f2053', 'id': '54a54bd2-4fd7-4129-a750-75b9f28a95b9'}

customer_id = '88b3ad90-3d48-460a-8698-16f8ff27a025'
group_obj = {'name': 'group_2', 'customer_id': customer_id}
ret = group_controller.create(admin_access_token, group_obj)
# {'name': 'group_2', 'customer_id': '88b3ad90-3d48-460a-8698-16f8ff27a025', 'id': '1a783634-1078-48a2-a085-48161548d184'}

# try with an existing one
ret = group_controller.create(admin_access_token, group_obj)
