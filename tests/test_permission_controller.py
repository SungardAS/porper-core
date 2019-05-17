
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

all_groups = []
for group in group_controller.find(admin_access_token, {}):
    all_groups.append(group['id'])

public_groups = []
for group in group_controller.find(public_access_token, {}):
    public_groups.append(group['id'])

non_public_groups = []
for group_id in all_groups:
    if group_id not in public_groups:
        non_public_groups.append(group_id)

from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(dynamodb)

# operations using admin user
params = {
    'resource_name': 'sla',
    'resource_id': 'first',
    'permissions': [{'action': 'r'}, {'action': 'w'}],
    #'to_group_id': <one_group>
    'to_group_ids': non_public_groups[:2]
}
permission_controller.create(admin_access_token, params)

params = {
    'action': 'r',
    'resource': 'sla',
    #'value': resource_id
    'value_only': True
}
ret = permission_controller.find(admin_access_token, params)
print(ret)


# operations using public user
params = {
    'resource_name': 'sla',
    'resource_id': 'first',
    'permissions': [{'action': 'r'}, {'action': 'w'}],
    #'to_group_id': <one_group>
    'to_group_ids': public_groups
}
permission_controller.create(public_access_token, params)

params = {
    'action': 'w',
    'resource': 'sla',
    #'value': resource_id,
    'value_only': True
}
ret = permission_controller.find(public_access_token, params)
print(ret)
