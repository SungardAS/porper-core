
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

# find a group
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)
groups = group_controller.find(admin_access_token, {})

### Invite a user
from porper.controllers.invited_user_controller import InvitedUserController
invited_user_controller = InvitedUserController(dynamodb)

email_address = "alex.ough@gmail.com"
item = {'email': email_address, 'group_id': groups[0]['id'], 'is_admin': False, 'auth_type': 'google'}
ret = invited_user_controller.create(admin_access_token, item)
# {'email': 'alex.ough@gmail.com', 'group_id': '54a54bd2-4fd7-4129-a750-75b9f28a95b9', 'is_admin': False, 'auth_type': 'google', 'invited_by': '35925', 'invited_at': '2019-04-18 01:05:31.196650', 'state': 'invited'}

email_address = "alex.ough@sungardas.com"
item = {'email': email_address, 'group_id': groups[1]['id'], 'is_admin': False, 'auth_type': 'cognito'}
ret = invited_user_controller.create(admin_access_token, item)
# {'email': 'alex.ough@sungardas.com', 'group_id': '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a', 'is_admin': False, 'auth_type': 'cognito', 'invited_by': '35925', 'invited_at': '2019-04-18 01:09:44.323468', 'state': 'invited'}

ret = invited_user_controller.find(admin_access_token, {})

ret = invited_user_controller.find(admin_access_token, {'email': email_address, 'auth_type': 'cognito'})

ret = invited_user_controller.find(admin_access_token, {'state': 'invited'})

# cancel invitation
item = {'email': "alex.ough@sungardas.com", 'auth_type': 'cognito'}
ret = invited_user_controller.delete(admin_access_token, item)

ret = invited_user_controller.find(admin_access_token, {'state': 'invited'})

# re-send invitation
item = {'email': "alex.ough@sungardas.com", 'auth_type': 'cognito'}
ret = invited_user_controller.update(admin_access_token, item)

ret = invited_user_controller.find(admin_access_token, {'state': 'invited'})
