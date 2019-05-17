
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
from porper.controllers.meta_resource_controller import ADMIN_GROUP_ID, PUBLIC_GROUP_ID

from util import find_token
admin_access_token = find_token(ADMIN_GROUP_ID)
public_access_token = find_token(PUBLIC_GROUP_ID)

from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)
admin_groups = group_controller.find(admin_access_token, {})
public_groups = group_controller.find(public_access_token, {})

from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(dynamodb)

# operations using admin user
resource_name = 'sla'
resource_id = 'first'
permissions = [{'action': 'r'}, {'action': 'w'}]
to_group_id = admin_groups[0]['id']
permission_controller.add_permissions_to_group(resource_name, resource_id, permissions, to_group_id)

params = {
    'action': 'r',
    'resource': resource_name,
    #'value': resource_id
    'value_only': True
}
ret = permission_controller.find(admin_access_token, params)
print(ret)


# operations using public user
resource_name = 'sla'
resource_id = 'second'
permissions = [{'action': 'r'}, {'action': 'w'}]
to_group_id = public_groups[0]['id']
permission_controller.add_permissions_to_group(resource_name, resource_id, permissions, to_group_id)

params = {
    'action': 'w',
    'resource': resource_name,
    #'value': resource_id,
    'value_only': True
}
ret = permission_controller.find(public_access_token, params)
print(ret)
