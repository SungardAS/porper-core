
import sys
sys.path.append('../..')

import os
import boto3
region = os.environ.get('AWS_DEFAULT_REGION')
dynamodb = boto3.resource('dynamodb',region_name=region)

import uuid
import datetime

ADMIN_GROUP_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'

#########################################################################################################
# Preparation
#########################################################################################################
### Create a first user, admin
# We'll use model classes because we don't have any access_token
# after the admin user is created, create an access_token for following tests
from porper.models.user import User
from porper.models.user_group import UserGroup
from porper.models.access_token import AccessToken
user = User(dynamodb)
user_group = UserGroup(dynamodb)
access_token = AccessToken(dynamodb)

admin_user = {
  "auth_type": "sso",
  "email": "admin.user@sungardas.com",
  "family_name": "Admin",
  "given_name": "User",
  "id": str(uuid.uuid4()),
  "name": "Admin User"
}
user_ret = user.create(admin_user)
group_ret = user_group.create({'user_id': user_ret['id'], 'group_id': ADMIN_GROUP_ID, 'is_admin': True})

admin_token = {
  "access_token": str(uuid.uuid4()),
  "refresh_token": str(uuid.uuid4()),
  "refreshed_time": str(datetime.datetime.now()),
  "user_id": user_ret['id']
}
admin_token_ret = access_token.create(admin_token)
# {'access_token': 'dc2a02a2-1508-43a8-a625-925873e88076', 'user_id': 'e20adc96-fcb6-4cb3-b376-f15bc8776c4f', 'refreshed_time': '2018-06-13 13:12:02.599955', 'refresh_token': '9b17b8b9-d8fc-4fa8-aec2-af4211c75fd4', 'time_stamp': '1528913522'}


#########################################################################################################
# Group management
#########################################################################################################
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)

### Create at least 3 groups
#  - Test user
#    - admin
group_1 = {'name': 'group_1'}
group_1_ret = group_controller.create(admin_token_ret['access_token'], group_1)
# {'name': 'group_1', 'id': '3df63285-5825-4991-95bb-2907e8eac688'}

group_2 = {'name': 'group_2'}
group_2_ret = group_controller.create(admin_token_ret['access_token'], group_2)
# {'name': 'group_2', 'id': 'fc986ae8-638a-481f-89c9-cc84e2483c7d'}

group_3 = {'name': 'group_3'}
group_3_ret = group_controller.create(admin_token_ret['access_token'], group_3)
# {'name': 'group_3', 'id': 'c484e72e-50f6-46f9-89fd-70cbf5cb2b5c'}


#########################################################################################################
# User Invitation & Authentication
#########################################################################################################
"""
admin_token_ret = {'access_token': 'dc2a02a2-1508-43a8-a625-925873e88076', 'user_id': 'e20adc96-fcb6-4cb3-b376-f15bc8776c4f', 'refreshed_time': '2018-06-13 13:12:02.599955', 'refresh_token': '9b17b8b9-d8fc-4fa8-aec2-af4211c75fd4', 'time_stamp': '1528913522'}
group_1_ret = {'name': 'group_1', 'id': '3df63285-5825-4991-95bb-2907e8eac688'}
group_2_ret = {'name': 'group_2', 'id': 'fc986ae8-638a-481f-89c9-cc84e2483c7d'}
group_3_ret = {'name': 'group_3', 'id': 'c484e72e-50f6-46f9-89fd-70cbf5cb2b5c'}
"""
from porper.controllers.invited_user_controller import InvitedUserController
invited_user_controller = InvitedUserController(dynamodb)

### invite an admin user for each group
#  - Test user
#    - admin
invited_group_admin_in_group_1 = {
    "auth_type": "sso",
    "email": "group_1.admin@sungardas.com",
    "group_id": group_1_ret['id'],
    "is_admin": True
}
invited_group_admin_in_group_1_ret = invited_user_controller.create(admin_token_ret['access_token'], invited_group_admin_in_group_1)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 19:11:38.129452', 'invited_by': u'e20adc96-fcb6-4cb3-b376-f15bc8776c4f', 'state': 'invited', 'is_admin': False, 'group_id': '3df63285-5825-4991-95bb-2907e8eac688', 'email': 'group_1.admin@sungardas.com'}

invited_group_admin_in_group_2 = {
    "auth_type": "sso",
    "email": "group_2.admin@sungardas.com",
    "group_id": group_2_ret['id'],
    "is_admin": True
}
invited_group_admin_in_group_2_ret = invited_user_controller.create(admin_token_ret['access_token'], invited_group_admin_in_group_2)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 19:14:05.242948', 'invited_by': u'e20adc96-fcb6-4cb3-b376-f15bc8776c4f', 'state': 'invited', 'is_admin': True, 'group_id': 'fc986ae8-638a-481f-89c9-cc84e2483c7d', 'email': 'group_2.admin@sungardas.com'}

invited_group_admin_in_group_3 = {
    "auth_type": "sso",
    "email": "group_3.admin@sungardas.com",
    "group_id": group_3_ret['id'],
    "is_admin": True
}
invited_group_admin_in_group_3_ret = invited_user_controller.create(admin_token_ret['access_token'], invited_group_admin_in_group_3)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 19:14:56.403604', 'invited_by': u'e20adc96-fcb6-4cb3-b376-f15bc8776c4f', 'state': 'invited', 'is_admin': True, 'group_id': 'c484e72e-50f6-46f9-89fd-70cbf5cb2b5c', 'email': 'group_3.admin@sungardas.com'}


### authenticate 3 new admin users to register
#  - Test user
#    - no access_token necessary
"""
invited_group_admin_in_group_1_ret = {'auth_type': 'sso', 'invited_at': '2018-06-13 19:11:38.129452', 'invited_by': u'e20adc96-fcb6-4cb3-b376-f15bc8776c4f', 'state': 'invited', 'is_admin': False, 'group_id': '3df63285-5825-4991-95bb-2907e8eac688', 'email': 'group_1.admin@sungardas.com'}
invited_group_admin_in_group_2_ret = {'auth_type': 'sso', 'invited_at': '2018-06-13 19:14:05.242948', 'invited_by': u'e20adc96-fcb6-4cb3-b376-f15bc8776c4f', 'state': 'invited', 'is_admin': True, 'group_id': 'fc986ae8-638a-481f-89c9-cc84e2483c7d', 'email': 'group_2.admin@sungardas.com'}
invited_group_admin_in_group_3_ret = {'auth_type': 'sso', 'invited_at': '2018-06-13 19:14:56.403604', 'invited_by': u'e20adc96-fcb6-4cb3-b376-f15bc8776c4f', 'state': 'invited', 'is_admin': True, 'group_id': 'c484e72e-50f6-46f9-89fd-70cbf5cb2b5c', 'email': 'group_3.admin@sungardas.com'}
"""
from porper.controllers.auth_controller import AuthController
auth_controller = AuthController(dynamodb)

invited_group_admin_in_group_1_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': invited_group_admin_in_group_1_ret['email'],
    'family_name': "Group_1",
    'given_name': "Admin",
    'name': "Group1 Admin",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
group_admin_in_group_1_ret = auth_controller.authenticate(invited_group_admin_in_group_1_auth_params)
# {'access_token': 'f58ca2c9-506d-4b70-a962-8b931e52e9cc', 'user_id': '1526672e-cf76-45be-abfe-c4f5938034e4', 'refreshed_time': '2018-06-13 19:29:01.635886', 'refresh_token': 'cb962a36-7f88-4319-a661-1e559ec4e343'}

invited_group_admin_in_group_2_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': invited_group_admin_in_group_2_ret['email'],
    'family_name': "Group_2",
    'given_name': "Admin",
    'name': "Group2 Admin",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
group_admin_in_group_2_ret = auth_controller.authenticate(invited_group_admin_in_group_2_auth_params)
# {'access_token': 'e4950ad0-f1de-484b-8c9b-73702ddf1a0a', 'user_id': 'c2075261-da71-4a74-8b7a-117215da8612', 'refreshed_time': '2018-06-13 19:35:21.781217', 'refresh_token': 'd72ec598-2d81-4681-8f85-4c126ee97384', 'time_stamp': '1528936521'}

invited_group_admin_in_group_3_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': invited_group_admin_in_group_3_ret['email'],
    'family_name': "Group_3",
    'given_name': "Admin",
    'name': "Group3 Admin",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
group_admin_in_group_3_ret = auth_controller.authenticate(invited_group_admin_in_group_3_auth_params)
# {'access_token': '427ae3eb-1fad-4ab7-911b-a7f35a74c4af', 'user_id': '848e749a-0b2a-49d9-b254-97fbb4723812', 'refreshed_time': '2018-06-13 19:36:32.493993', 'refresh_token': '75d7620b-7ca6-4b6d-abcc-18d22807ebc4', 'time_stamp': '1528936592'}


### invite an admin and a user for each group
#  - Test user
#    - each group admin
"""
group_admin_in_group_1_ret = {'access_token': 'f58ca2c9-506d-4b70-a962-8b931e52e9cc', 'user_id': '1526672e-cf76-45be-abfe-c4f5938034e4', 'refreshed_time': '2018-06-13 19:29:01.635886', 'refresh_token': 'cb962a36-7f88-4319-a661-1e559ec4e343'}
group_admin_in_group_2_ret = {'access_token': 'e4950ad0-f1de-484b-8c9b-73702ddf1a0a', 'user_id': 'c2075261-da71-4a74-8b7a-117215da8612', 'refreshed_time': '2018-06-13 19:35:21.781217', 'refresh_token': 'd72ec598-2d81-4681-8f85-4c126ee97384', 'time_stamp': '1528936521'}
group_admin_in_group_3_ret = {'access_token': '427ae3eb-1fad-4ab7-911b-a7f35a74c4af', 'user_id': '848e749a-0b2a-49d9-b254-97fbb4723812', 'refreshed_time': '2018-06-13 19:36:32.493993', 'refresh_token': '75d7620b-7ca6-4b6d-abcc-18d22807ebc4', 'time_stamp': '1528936592'}
"""
from porper.controllers.invited_user_controller import InvitedUserController
invited_user_controller = InvitedUserController(dynamodb)

invited_group_admin_2_in_group_1 = {
    "auth_type": "sso",
    "email": "group_1.admin_2@sungardas.com",
    "group_id": group_1_ret['id'],
    "is_admin": True
}
invited_group_admin_2_in_group_1_ret = invited_user_controller.create(group_admin_in_group_1_ret['access_token'], invited_group_admin_2_in_group_1)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 19:57:07.210192', 'invited_by': u'1526672e-cf76-45be-abfe-c4f5938034e4', 'state': 'invited', 'is_admin': True, 'group_id': '3df63285-5825-4991-95bb-2907e8eac688', 'email': 'group_1.admin_2@sungardas.com'}

invited_user_in_group_1 = {
    "auth_type": "sso",
    "email": "group_1.user@sungardas.com",
    "group_id": group_1_ret['id'],
    "is_admin": False
}
invited_user_in_group_1_ret = invited_user_controller.create(group_admin_in_group_1_ret['access_token'], invited_user_in_group_1)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 19:57:37.045028', 'invited_by': u'1526672e-cf76-45be-abfe-c4f5938034e4', 'state': 'invited', 'is_admin': False, 'group_id': '3df63285-5825-4991-95bb-2907e8eac688', 'email': 'group_1.user@sungardas.com'}

invited_group_admin_2_in_group_2 = {
    "auth_type": "sso",
    "email": "group_2.admin_2@sungardas.com",
    "group_id": group_2_ret['id'],
    "is_admin": True
}
invited_group_admin_2_in_group_2_ret = invited_user_controller.create(group_admin_in_group_2_ret['access_token'], invited_group_admin_2_in_group_2)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 19:58:48.229028', 'invited_by': u'c2075261-da71-4a74-8b7a-117215da8612', 'state': 'invited', 'is_admin': True, 'group_id': 'fc986ae8-638a-481f-89c9-cc84e2483c7d', 'email': 'group_2.admin_2@sungardas.com'}

invited_user_in_group_2 = {
    "auth_type": "sso",
    "email": "group_2.user@sungardas.com",
    "group_id": group_2_ret['id'],
    "is_admin": False
}
invited_user_in_group_2_ret = invited_user_controller.create(group_admin_in_group_2_ret['access_token'], invited_user_in_group_2)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 19:59:17.511575', 'invited_by': u'c2075261-da71-4a74-8b7a-117215da8612', 'state': 'invited', 'is_admin': False, 'group_id': 'fc986ae8-638a-481f-89c9-cc84e2483c7d', 'email': 'group_2.user@sungardas.com'}

invited_group_admin_2_in_group_3 = {
    "auth_type": "sso",
    "email": "group_3.admin_2@sungardas.com",
    "group_id": group_3_ret['id'],
    "is_admin": True
}
invited_group_admin_2_in_group_3_ret = invited_user_controller.create(group_admin_in_group_3_ret['access_token'], invited_group_admin_2_in_group_3)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 22:52:52.509162', 'invited_by': u'848e749a-0b2a-49d9-b254-97fbb4723812', 'state': 'invited', 'is_admin': True, 'group_id': 'c484e72e-50f6-46f9-89fd-70cbf5cb2b5c', 'email': 'group_3.admin_2@sungardas.com'}

invited_user_in_group_3 = {
    "auth_type": "sso",
    "email": "group_3.user@sungardas.com",
    "group_id": group_3_ret['id'],
    "is_admin": False
}
invited_user_in_group_3_ret = invited_user_controller.create(group_admin_in_group_3_ret['access_token'], invited_user_in_group_3)
# {'auth_type': 'sso', 'invited_at': '2018-06-13 22:53:15.187480', 'invited_by': u'848e749a-0b2a-49d9-b254-97fbb4723812', 'state': 'invited', 'is_admin': False, 'group_id': 'c484e72e-50f6-46f9-89fd-70cbf5cb2b5c', 'email': 'group_3.user@sungardas.com'}


### authenticate 3 new users to register
#  - Test user
#    - no access_token necessary
"""
invited_user_in_group_1_ret = {'auth_type': 'sso', 'invited_at': '2018-06-13 19:57:37.045028', 'invited_by': u'1526672e-cf76-45be-abfe-c4f5938034e4', 'state': 'invited', 'is_admin': False, 'group_id': '3df63285-5825-4991-95bb-2907e8eac688', 'email': 'group_1.user@sungardas.com'}
invited_user_in_group_2_ret = {'auth_type': 'sso', 'invited_at': '2018-06-13 19:59:17.511575', 'invited_by': u'c2075261-da71-4a74-8b7a-117215da8612', 'state': 'invited', 'is_admin': False, 'group_id': 'fc986ae8-638a-481f-89c9-cc84e2483c7d', 'email': 'group_2.user@sungardas.com'}
invited_user_in_group_3_ret = {'auth_type': 'sso', 'invited_at': '2018-06-13 22:53:15.187480', 'invited_by': u'848e749a-0b2a-49d9-b254-97fbb4723812', 'state': 'invited', 'is_admin': False, 'group_id': 'c484e72e-50f6-46f9-89fd-70cbf5cb2b5c', 'email': 'group_3.user@sungardas.com'}
"""
from porper.controllers.auth_controller import AuthController
auth_controller = AuthController(dynamodb)

invited_user_in_group_1_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': invited_user_in_group_1_ret['email'],
    'family_name': "Group_1",
    'given_name': "User",
    'name': "Group_1 User",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
user_in_group_1_ret = auth_controller.authenticate(invited_user_in_group_1_auth_params)
# {'access_token': 'f15ca8f6-043d-48a7-8171-dd28c16ba6f6', 'user_id': 'e07e35e3-1c15-458c-82c5-0157bf78fe2b', 'refreshed_time': '2018-06-13 23:06:05.386205', 'refresh_token': '7c9cb29c-0ae5-4137-be76-a35cd2743c98', 'time_stamp': '1528949165'}

invited_user_in_group_2_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': invited_user_in_group_2_ret['email'],
    'family_name': "Group_2",
    'given_name': "User",
    'name': "Group_2 User",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
user_in_group_2_ret = auth_controller.authenticate(invited_user_in_group_2_auth_params)
# {'access_token': '2316b519-4e3a-4677-83de-9d13faea2996', 'user_id': '3cb8fc57-1c9a-48c0-93d5-beeb37ebe5c3', 'refreshed_time': '2018-06-13 23:07:28.048722', 'refresh_token': 'd8826ab0-9d35-4892-a66a-e6902b30b485', 'time_stamp': '1528949248'}

invited_user_in_group_3_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': invited_user_in_group_3_ret['email'],
    'family_name': "Group_3",
    'given_name': "User",
    'name': "Group_3 User",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
user_in_group_3_ret = auth_controller.authenticate(invited_user_in_group_3_auth_params)
# {'access_token': 'cf0d6f46-2aad-4f2b-a9ac-f9d44ad3368f', 'user_id': 'c9ac789a-28b0-41b2-b7fc-f4d56db42917', 'refreshed_time': '2018-06-13 23:08:20.069503', 'refresh_token': 'a6814338-f0a4-44a3-b594-6d1facda83d0', 'time_stamp': '1528949300'}


### invite another new user for each group
#  - Test user
#    - user
"""
user_in_group_1_ret = {'access_token': 'f15ca8f6-043d-48a7-8171-dd28c16ba6f6', 'user_id': 'e07e35e3-1c15-458c-82c5-0157bf78fe2b', 'refreshed_time': '2018-06-13 23:06:05.386205', 'refresh_token': '7c9cb29c-0ae5-4137-be76-a35cd2743c98', 'time_stamp': '1528949165'}
user_in_group_2_ret = {'access_token': '2316b519-4e3a-4677-83de-9d13faea2996', 'user_id': '3cb8fc57-1c9a-48c0-93d5-beeb37ebe5c3', 'refreshed_time': '2018-06-13 23:07:28.048722', 'refresh_token': 'd8826ab0-9d35-4892-a66a-e6902b30b485', 'time_stamp': '1528949248'}
user_in_group_3_ret = {'access_token': 'cf0d6f46-2aad-4f2b-a9ac-f9d44ad3368f', 'user_id': 'c9ac789a-28b0-41b2-b7fc-f4d56db42917', 'refreshed_time': '2018-06-13 23:08:20.069503', 'refresh_token': 'a6814338-f0a4-44a3-b594-6d1facda83d0', 'time_stamp': '1528949300'}
"""
from porper.controllers.invited_user_controller import InvitedUserController
invited_user_controller = InvitedUserController(dynamodb)

invited_user_2_in_group_1 = {
    "auth_type": "sso",
    "email": "group_1.user_2@sungardas.com",
    "group_id": group_1_ret['id'],
    "is_admin": False
}
try:
    invited_user_2_in_group_1_ret = invited_user_controller.create(user_in_group_1_ret['access_token'], invited_user_2_in_group_1)
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

invited_user_2_in_group_2 = {
    "auth_type": "sso",
    "email": "group_2.user_2@sungardas.com",
    "group_id": group_2_ret['id'],
    "is_admin": False
}
try:
    invited_user_2_in_group_2_ret = invited_user_controller.create(user_in_group_2_ret['access_token'], invited_user_2_in_group_2)
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

invited_user_2_in_group_3 = {
    "auth_type": "sso",
    "email": "group_3.user_2@sungardas.com",
    "group_id": group_3_ret['id'],
    "is_admin": False
}
try:
    invited_user_2_in_group_3_ret = invited_user_controller.create(user_in_group_3_ret['access_token'], invited_user_2_in_group_3)
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex


### authenticate non-invited user
#  - Test user
#    - no access_token necessary
from porper.controllers.auth_controller import AuthController
auth_controller = AuthController(dynamodb)

uninvited_user_in_group_1_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': 'group_1.uninvited@sungardas.com',
    'family_name': "Group_1",
    'given_name': "Uninvited",
    'name': "Group_1 Uninvited",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
try:
    uninvited_user_in_group_1_ret = auth_controller.authenticate(uninvited_user_in_group_1_auth_params)
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "Please invite this user first":
        pass
    else:
        raise ex


#########################################################################################################
# Add User to Group
#########################################################################################################
from porper.controllers.user_controller import UserController
user_controller = UserController(dynamodb)

### create
#  - Test user
#    - admin

# add the group admin of one group to diff group as user
user_controller.create(admin_token_ret['access_token'], {'id': group_admin_in_group_1_ret['user_id'], 'group_id': group_2_ret['id'], 'is_admin': False})


### create
#  - Test user
#    - group admin

# 1. add the user of diff group to the test user's group as group admin
user_controller.create(group_admin_in_group_2_ret['access_token'], {'id': user_in_group_1_ret['user_id'], 'group_id': group_2_ret['id'], 'is_admin': True})

# 2. add the user of the test user's group to diff group as group admin
try:
    user_controller.create(group_admin_in_group_2_ret['access_token'], {'id': user_in_group_2_ret['user_id'], 'group_id': group_1_ret['id'], 'is_admin': True})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex


### create
#  - Test user
#    - user

# 1. add the user of diff group to the test user's group as group admin
try:
    user_controller.create(user_in_group_2_ret['access_token'], {'id': user_in_group_1_ret['user_id'], 'group_id': group_2_ret['id'], 'is_admin': True})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2. add the user of the test user's group to diff group as group admin
try:
    user_controller.create(user_in_group_2_ret['access_token'], {'id': user_in_group_2_ret['user_id'], 'group_id': group_1_ret['id'], 'is_admin': True})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex


#### In Create in User
# 'group_admin_in_group_1_ret' was added to 'group_2_ret' as a user
# 'user_in_group_1_ret' was added to 'group_2_ret' as an admin

####
# 'group_1_ret'
#   - 'group_admin_in_group_1_ret' as admin
#   - 'user_in_group_1_ret' as user
# 'group_2_ret'
#   - 'group_admin_in_group_2_ret' as admin
#   - 'user_in_group_1_ret' as admin
#   - 'group_admin_in_group_1_ret' as user
#   - 'user_in_group_2_ret' as user
# 'group_3_ret'
#   - 'group_admin_in_group_3_ret' as admin
#   - 'user_in_group_3_ret' as user

#########################################################################################################
# Find User
#########################################################################################################
from porper.controllers.user_controller import UserController
user_controller = UserController(dynamodb)

### find user
#  - Test user
#    - admin

# 1. input params: None
num_create_users = 7
users = user_controller.find(admin_token_ret['access_token'], {})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 2. input params: group_id
num_create_users = 4
users = user_controller.find(admin_token_ret['access_token'], {'group_id': group_2_ret['id']})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 3. input params: ids
ids = [group_admin_in_group_1_ret['user_id'], user_in_group_2_ret['user_id']]
num_create_users = len(ids)
users = user_controller.find(admin_token_ret['access_token'], {'ids': ids})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 4. input params: id
id = group_admin_in_group_3_ret['user_id']
user_controller.find(admin_token_ret['access_token'], {'id': id})

# 5. input params: email, auth
params = {
    'email': invited_group_admin_in_group_1_auth_params['email'],
    'auth_type': invited_group_admin_in_group_1_auth_params['auth_type']
}
users = user_controller.find(admin_token_ret['access_token'], params)
print("there are {} users".format(len(users)))
if users[0]['email'] != params['email'] or users[0]['auth_type'] != params['auth_type']:
    raise Exception("The returned user is not same with the given")


### find user
#  - Test user
#    - group admin

# 1. input params: None
num_create_users = 4
users = user_controller.find(group_admin_in_group_1_ret['access_token'], {})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 2-1. input params: group_id (test user's group)
num_create_users = 4
users = user_controller.find(group_admin_in_group_2_ret['access_token'], {'group_id': group_2_ret['id']})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 2-2. input params: group_id (group where this test user does NOT belong)
num_create_users = 0
users = user_controller.find(group_admin_in_group_1_ret['access_token'], {'group_id': group_3_ret['id']})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 3-1. input params: ids (ids in the same group)
ids = [group_admin_in_group_2_ret['user_id'], user_in_group_2_ret['user_id']]
num_create_users = len(ids)
users = user_controller.find(group_admin_in_group_2_ret['access_token'], {'ids': ids})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 3-2. input params: ids (some in the same group and some in the diff group)
ids = [
    group_admin_in_group_2_ret['user_id'],
    user_in_group_2_ret['user_id'],
    group_admin_in_group_3_ret['user_id'],
    user_in_group_3_ret['user_id']
]
num_create_users = 2
users = user_controller.find(group_admin_in_group_3_ret['access_token'], {'ids': ids})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 3-3. input params: ids (all in the diff group)
ids = [
    group_admin_in_group_1_ret['user_id'],
    user_in_group_1_ret['user_id'],
    group_admin_in_group_2_ret['user_id'],
    user_in_group_2_ret['user_id']
]
num_create_users = 0
users = user_controller.find(group_admin_in_group_3_ret['access_token'], {'ids': ids})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 4-1. input params: id (in the same group, and using access_token of different user in the same group)
id = user_in_group_1_ret['user_id']
user_controller.find(group_admin_in_group_1_ret['access_token'], {'id': id})

# 4-2. input params: id (in the same group, and using access_token of the same user)
id = group_admin_in_group_1_ret['user_id']
user_controller.find(group_admin_in_group_1_ret['access_token'], {'id': id})

# 4-3. input params: id (in the dfferent group)
id = group_admin_in_group_2_ret['user_id']
try:
    user_controller.find(group_admin_in_group_3_ret['access_token'], {'id': id})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 5-1. input params: email, auth (in the same group, and using access_token of different user in the same group)
params = {
    'email': invited_user_in_group_1_auth_params['email'],
    'auth_type': invited_user_in_group_1_auth_params['auth_type']
}
users = user_controller.find(group_admin_in_group_1_ret['access_token'], params)
print("there are {} users".format(len(users)))
if users[0]['email'] != params['email'] or users[0]['auth_type'] != params['auth_type']:
    raise Exception("The returned user is not same with the given")

# 5-2. input params: email, auth (in the same group, using access_token of the same user)
params = {
    'email': invited_group_admin_in_group_1_auth_params['email'],
    'auth_type': invited_group_admin_in_group_1_auth_params['auth_type']
}
users = user_controller.find(group_admin_in_group_1_ret['access_token'], params)
print("there are {} users".format(len(users)))
if users[0]['email'] != params['email'] or users[0]['auth_type'] != params['auth_type']:
    raise Exception("The returned user is not same with the given")

# 5-3. input params: id (in the dfferent group)
params = {
    'email': invited_group_admin_in_group_2_auth_params['email'],
    'auth_type': invited_group_admin_in_group_2_auth_params['auth_type']
}
num_create_users = 0
users = user_controller.find(group_admin_in_group_3_ret['access_token'], params)
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))


### find user
#  - Test user
#    - user

# 1. input params: None
num_create_users = 4
users = user_controller.find(user_in_group_1_ret['access_token'], {})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 2-1. input params: group_id (test user's group)
num_create_users = 4
users = user_controller.find(user_in_group_2_ret['access_token'], {'group_id': group_2_ret['id']})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 2-2. input params: group_id (group where this test user does NOT belong)
num_create_users = 0
users = user_controller.find(user_in_group_3_ret['access_token'], {'group_id': group_1_ret['id']})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 3-1. input params: ids (ids in the same group)
ids = [group_admin_in_group_2_ret['user_id'], user_in_group_2_ret['user_id']]
num_create_users = len(ids)
users = user_controller.find(user_in_group_2_ret['access_token'], {'ids': ids})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 3-2. input params: ids (some in the same group and some in the diff group)
ids = [
    group_admin_in_group_2_ret['user_id'],
    user_in_group_2_ret['user_id'],
    group_admin_in_group_3_ret['user_id'],
    user_in_group_3_ret['user_id']
]
num_create_users = 2
users = user_controller.find(user_in_group_3_ret['access_token'], {'ids': ids})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 3-3. input params: ids (all in the diff group)
ids = [
    group_admin_in_group_1_ret['user_id'],
    user_in_group_1_ret['user_id'],
    group_admin_in_group_2_ret['user_id'],
    user_in_group_2_ret['user_id']
]
num_create_users = 0
users = user_controller.find(user_in_group_3_ret['access_token'], {'ids': ids})
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))

# 4-1. input params: id (in the same group, and using access_token of different user in the same group)
id = group_admin_in_group_1_ret['user_id']
user_controller.find(user_in_group_1_ret['access_token'], {'id': id})

# 4-2. input params: id (in the same group, and using access_token of the same user)
id = user_in_group_2_ret['user_id']
user_controller.find(user_in_group_2_ret['access_token'], {'id': id})

# 4-3. input params: id (in the dfferent group)
id = user_in_group_2_ret['user_id']
try:
    user_controller.find(user_in_group_3_ret['access_token'], {'id': id})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 5-1. input params: email, auth (in the same group, and using access_token of different user in the same group)
params = {
    'email': invited_group_admin_in_group_1_auth_params['email'],
    'auth_type': invited_group_admin_in_group_1_auth_params['auth_type']
}
users = user_controller.find(user_in_group_1_ret['access_token'], params)
print("there are {} users".format(len(users)))
if users[0]['email'] != params['email'] or users[0]['auth_type'] != params['auth_type']:
    raise Exception("The returned user is not same with the given")

# 5-2. input params: email, auth (in the same group, using access_token of the same user)
params = {
    'email': invited_user_in_group_2_auth_params['email'],
    'auth_type': invited_user_in_group_2_auth_params['auth_type']
}
users = user_controller.find(user_in_group_2_ret['access_token'], params)
print("there are {} users".format(len(users)))
if users[0]['email'] != params['email'] or users[0]['auth_type'] != params['auth_type']:
    raise Exception("The returned user is not same with the given")

# 5-3. input params: id (in the dfferent group)
params = {
    'email': invited_group_admin_in_group_2_auth_params['email'],
    'auth_type': invited_group_admin_in_group_2_auth_params['auth_type']
}
num_create_users = 0
users = user_controller.find(user_in_group_3_ret['access_token'], params)
print("there are {} users".format(len(users)))
if len(users) != num_create_users:
    raise Exception("number of users should be {}".format(num_create_users))


#### In Create in User
# 'group_admin_in_group_1_ret' was added to 'group_2_ret' as a user
# 'user_in_group_1_ret' was added to 'group_2_ret' as an admin

####
# 'group_1_ret'
#   - 'group_admin_in_group_1_ret' as admin
#   - 'user_in_group_1_ret' as user
# 'group_2_ret'
#   - 'group_admin_in_group_2_ret' as admin
#   - 'user_in_group_1_ret' as admin
#   - 'group_admin_in_group_1_ret' as user
#   - 'user_in_group_2_ret' as user
# 'group_3_ret'
#   - 'group_admin_in_group_3_ret' as admin
#   - 'user_in_group_3_ret' as user

#########################################################################################################
# Delete User (remove users from groups)
#########################################################################################################
from porper.controllers.user_controller import UserController
user_controller = UserController(dynamodb)

### remove
#  - Test user
#    - admin

# 1-1. remove the test admin itself from an admin group where there are more than one admins
# first, add a new admin to the admin group before testing before removing this test user
user_controller.create(admin_token_ret['access_token'], {'id': group_admin_in_group_1_ret['user_id'], 'group_id': ADMIN_GROUP_ID, 'is_admin': False})
user_controller.delete(admin_token_ret['access_token'], {'id': admin_token_ret['user_id'], 'group_id': ADMIN_GROUP_ID, 'is_admin': False})

# 1-2. remove another admin from an admin group
# first, put back the original admin to the admin group and delete the other admin
user_controller.create(group_admin_in_group_1_ret['access_token'], {'id': admin_token_ret['user_id'], 'group_id': ADMIN_GROUP_ID, 'is_admin': False})
user_controller.delete(admin_token_ret['access_token'], {'id': group_admin_in_group_1_ret['user_id'], 'group_id': ADMIN_GROUP_ID})

# 1-3. remove the test admin itself from an admin group where there is only one admin
try:
    user_controller.delete(admin_token_ret['access_token'], {'id': admin_token_ret['user_id'], 'group_id': ADMIN_GROUP_ID})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "You cannot remove this user because there must be at least one user in admin group":
        pass
    else:
        raise ex

# 2-1. remove a group admin from its group where there is only one group admin
user_controller.delete(admin_token_ret['access_token'], {'id': group_admin_in_group_1_ret['user_id'], 'group_id': group_1_ret['id']})

# 2-2. remove a group admin from its group where there are more than one group admins
user_controller.delete(admin_token_ret['access_token'], {'id': group_admin_in_group_2_ret['user_id'], 'group_id': group_2_ret['id']})

# 3-1. remove a user from a group where there is only one user including grop admin
user_controller.delete(admin_token_ret['access_token'], {'id': user_in_group_1_ret['user_id'], 'group_id': group_1_ret['id']})

# 3-2. remove a user from a group where there are more than one user including grop admin
user_controller.delete(admin_token_ret['access_token'], {'id': user_in_group_2_ret['user_id'], 'group_id': group_2_ret['id']})


####
# 'group_1_ret'
#   - None
# 'group_2_ret'
#   - 'user_in_group_1_ret' as admin
#   - 'group_admin_in_group_1_ret' as user
# 'group_3_ret'
#   - 'group_admin_in_group_3_ret' as admin
#   - 'user_in_group_3_ret' as user

### remove
#  - Test user
#    - group admin

# 1. remove a admin from a admin group
try:
    user_controller.delete(group_admin_in_group_3_ret['access_token'], {'id': admin_token_ret['user_id'], 'group_id': ADMIN_GROUP_ID})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2-1. remove the test user itself from its group where there are more than one users including group admin
user_controller.delete(group_admin_in_group_3_ret['access_token'], {'id': group_admin_in_group_3_ret['user_id'], 'group_id': group_3_ret['id']})

# 2-2. remove the test user itself from its group where there is only one user including group admin
# first, delete an existing user to make the group have only the test user before removing the test user itself
user_controller.delete(user_in_group_1_ret['access_token'], {'id': group_admin_in_group_1_ret['user_id'], 'group_id': group_2_ret['id']})
user_controller.delete(user_in_group_1_ret['access_token'], {'id': user_in_group_1_ret['user_id'], 'group_id': group_2_ret['id']})

####
# 'group_1_ret'
#   - None
# 'group_2_ret'
#   - None
# 'group_3_ret'
#   - 'user_in_group_3_ret' as user

# 2-3. remove a group admin from a different group where there is only one user including group admin
# first, add group admins in two different groups before removing one of them by the other
user_controller.create(admin_token_ret['access_token'], {'id': user_in_group_1_ret['user_id'], 'group_id': group_2_ret['id'], 'is_admin': True})
user_controller.create(admin_token_ret['access_token'], {'id': group_admin_in_group_3_ret['user_id'], 'group_id': group_3_ret['id'], 'is_admin': True})
try:
    user_controller.delete(group_admin_in_group_3_ret['access_token'], {'id': user_in_group_1_ret['user_id'], 'group_id': group_2_ret['id']})
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2-4. remove a group admin from a different group where there are more than one user including group admin
try:
    user_controller.delete(user_in_group_1_ret['access_token'], {'id': group_admin_in_group_3_ret['user_id'], 'group_id': group_3_ret['id']})
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

####
# 'group_1_ret'
#   - None
# 'group_2_ret'
#   - user_in_group_1_ret as admin
# 'group_3_ret'
#   - group_admin_in_group_3_ret as admin
#   - 'user_in_group_3_ret' as user

# 3-1. remove a user from its group where there is only one user including group admin
# This is impossible because a normal user (who is the only user in the group) has no priviledge to remove users from a group

# 3-2. remove a user from its group where there are more than one users including group admin
user_controller.delete(group_admin_in_group_3_ret['access_token'], {'id': user_in_group_3_ret['user_id'], 'group_id': group_3_ret['id']})

# 3-3. remove a user from a different group where there is only one user including group admin
# first, add a normal user to a diff group before removing it
user_controller.create(admin_token_ret['access_token'], {'id': user_in_group_1_ret['user_id'], 'group_id': group_1_ret['id'], 'is_admin': False})
try:
    user_controller.delete(group_admin_in_group_2_ret['access_token'], {'id': user_in_group_1_ret['user_id'], 'group_id': group_1_ret['id']})
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 3-4. remove a user from a different group where there are more than one users including group admin
# first, add a normal user to a diff group before removing it
user_controller.create(admin_token_ret['access_token'], {'id': group_admin_in_group_1_ret['user_id'], 'group_id': group_2_ret['id'], 'is_admin': False})
try:
    user_controller.delete(group_admin_in_group_3_ret['access_token'], {'id': group_admin_in_group_1_ret['user_id'], 'group_id': group_2_ret['id']})
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex


####
# 'group_1_ret'
#   - user_in_group_1_ret as user
# 'group_2_ret'
#   - user_in_group_1_ret as admin
#   - group_admin_in_group_1_ret as user
# 'group_3_ret'
#   - group_admin_in_group_3_ret as admin

### remove
#  - Test user
#    - user

# 1. remove a admin from a admin group
try:
    user_controller.delete(user_in_group_3_ret['access_token'], {'id': admin_token_ret['user_id'], 'group_id': ADMIN_GROUP_ID})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2-1. remove a group admin from a different group where there is only one user including group admin
## TODO:

# 2-2. remove a group admin from a different group where there are more than one user including group admin
## TODO:

# 3-1. remove the test user itself from its group where there is only one user including group admin
## TODO:

# 3-2. remove the test user itself from its group where there are more than one users including group admin
## TODO:

# 3-3. remove a user from a different group where there is only one user including group admin
## TODO:

# 3-4. remove a user from a different group where there are more than one users including group admin
## TODO:


####
# 'group_1_ret'
#   - user_in_group_1_ret as user
# 'group_2_ret'
#   - user_in_group_1_ret as admin
#   - group_admin_in_group_1_ret as user
# 'group_3_ret'
#   - group_admin_in_group_3_ret as admin

# add 'user_in_group_2_ret' in 'group_2_ret' for 'Find group' tests
user_controller.create(user_in_group_1_ret['access_token'], {'id': user_in_group_2_ret['user_id'], 'group_id': group_2_ret['id'], 'is_admin': False})

####
# 'group_1_ret'
#   - user_in_group_1_ret as user
# 'group_2_ret'
#   - user_in_group_1_ret as admin
#   - group_admin_in_group_1_ret as user
#   - user_in_group_2_ret as user
# 'group_3_ret'
#   - group_admin_in_group_3_ret as admin

#########################################################################################################
# Find groups
#########################################################################################################
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)

### find group
#  - Test user
#    - admin

# 1. input params: None
num_create_groups = 5
groups = group_controller.find(admin_token_ret['access_token'], {})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 2. input params: user_id
num_create_groups = 2
groups = group_controller.find(admin_token_ret['access_token'], {'user_id': user_in_group_1_ret['user_id']})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 3. input params: ids
ids = [group_2_ret['id'], group_3_ret['id']]
num_create_groups = len(ids)
groups = group_controller.find(admin_token_ret['access_token'], {'ids': ids})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 4. input params: id
id = group_3_ret['id']
group_controller.find(admin_token_ret['access_token'], {'id': id})

# 5. input params: name
params = {
    'name': group_1_ret['name']
}
groups = group_controller.find(admin_token_ret['access_token'], params)
print("there are {} groups".format(len(groups)))
if groups[0]['name'] != params['name']:
    raise Exception("The returned group is not same with the given")


### find group
#  - Test user
#    - group admin

# 1. input params: None
num_create_groups = 2
groups = group_controller.find(user_in_group_1_ret['access_token'], {})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 2-1. input params: user_id (in test user's group)
num_create_groups = 1
groups = group_controller.find(user_in_group_1_ret['access_token'], {'user_id': group_admin_in_group_1_ret['user_id']})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 2-2. input params: user_id (in diff group)
num_create_groups = 0
groups = group_controller.find(user_in_group_1_ret['access_token'], {'user_id': group_admin_in_group_3_ret['user_id']})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 2-2. input params: user_id (who does NOT belong any group)
num_create_groups = 0
groups = group_controller.find(user_in_group_1_ret['access_token'], {'user_id': group_admin_in_group_2_ret['user_id']})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 3-1. input params: ids (groups where the test user belongs)
ids = [group_1_ret['id'], group_2_ret['id']]
num_create_groups = len(ids)
groups = group_controller.find(user_in_group_1_ret['access_token'], {'ids': ids})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 3-2. input params: ids (some groups where the test user belongs and some NOT belong)
ids = [
    group_2_ret['id'],
    group_3_ret['id']
]
num_create_groups = 1
groups = group_controller.find(user_in_group_1_ret['access_token'], {'ids': ids})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 3-3. input params: ids (all groups where the test user does NOT belong)
ids = [
    group_1_ret['id'],
    group_2_ret['id']
]
num_create_groups = 0
groups = group_controller.find(group_admin_in_group_3_ret['access_token'], {'ids': ids})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 4-1. input params: id (group where the test user belong)
id = group_2_ret['id']
group_controller.find(user_in_group_1_ret['access_token'], {'id': id})

# 4-2. input params: id (group where the test user does NOT belong)
id = group_1_ret['id']
try:
    group_controller.find(group_admin_in_group_3_ret['access_token'], {'id': id})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 5-1. input params: name (group where the test user belong)
params = {
    'name': group_2_ret['name']
}
groups = group_controller.find(user_in_group_1_ret['access_token'], params)
print("there are {} groups".format(len(groups)))
if groups[0]['name'] != params['name']:
    raise Exception("The returned group is not same with the given")

# 5-2. input params: name (group where the test user does NOT belong)
params = {
    'name': group_2_ret['name']
}
num_create_groups = 0
groups = group_controller.find(group_admin_in_group_3_ret['access_token'], params)
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))


### find group
#  - Test user
#    - user

# 1. input params: None
num_create_groups = 2
groups = group_controller.find(user_in_group_1_ret['access_token'], {})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 2-1. input params: user_id (in test user's group)
num_create_groups = 1
groups = group_controller.find(user_in_group_2_ret['access_token'], {'user_id': group_admin_in_group_1_ret['user_id']})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 2-2. input params: user_id (in diff group)
num_create_groups = 0
groups = group_controller.find(user_in_group_2_ret['access_token'], {'user_id': group_admin_in_group_3_ret['user_id']})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 2-2. input params: user_id (who does NOT belong any group)
num_create_groups = 0
groups = group_controller.find(user_in_group_2_ret['access_token'], {'user_id': group_admin_in_group_2_ret['user_id']})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 3-1. input params: ids (groups where the test user belongs)
ids = [group_2_ret['id']]
num_create_groups = len(ids)
groups = group_controller.find(user_in_group_2_ret['access_token'], {'ids': ids})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 3-2. input params: ids (some groups where the test user belongs and some NOT belong)
ids = [
    group_2_ret['id'],
    group_3_ret['id']
]
num_create_groups = 1
groups = group_controller.find(user_in_group_2_ret['access_token'], {'ids': ids})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 3-3. input params: ids (all groups where the test user does NOT belong)
ids = [
    group_1_ret['id'],
    group_3_ret['id']
]
num_create_groups = 0
groups = group_controller.find(user_in_group_2_ret['access_token'], {'ids': ids})
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))

# 4-1. input params: id (group where the test user belong)
id = group_2_ret['id']
group_controller.find(user_in_group_2_ret['access_token'], {'id': id})

# 4-2. input params: id (group where the test user does NOT belong)
id = group_3_ret['id']
try:
    group_controller.find(user_in_group_2_ret['access_token'], {'id': id})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 5-1. input params: name (group where the test user belong)
params = {
    'name': group_2_ret['name']
}
groups = group_controller.find(user_in_group_2_ret['access_token'], params)
print("there are {} groups".format(len(groups)))
if groups[0]['name'] != params['name']:
    raise Exception("The returned group is not same with the given")

# 5-2. input params: name (group where the test user does NOT belong)
params = {
    'name': group_3_ret['name']
}
num_create_groups = 0
groups = group_controller.find(user_in_group_2_ret['access_token'], params)
print("there are {} groups".format(len(groups)))
if len(groups) != num_create_groups:
    raise Exception("number of groups should be {}".format(num_create_groups))


#########################################################################################################
# Update groups
#########################################################################################################
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)

### update
#  - Test user
#    - admin

# 1. update the admin group
try:
    group_controller.update(admin_token_ret['access_token'], {'id': ADMIN_GROUP_ID, 'name': 'new_admin'})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "You cannot update the admin group":
        pass
    else:
        raise ex

# 2. update a normal group
group_controller.update(admin_token_ret['access_token'], {'id': group_2_ret['id'], 'name': 'new_group_2'})


### update
#  - Test user
#    - group admin

# 1. update the admin group
try:
    group_controller.update(group_admin_in_group_3_ret['access_token'], {'id': ADMIN_GROUP_ID, 'name': 'new_admin'})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "You cannot update the admin group":
        pass
    else:
        raise ex

# 2-1. update a group where the test user belongs
group_controller.update(group_admin_in_group_3_ret['access_token'], {'id': group_3_ret['id'], 'name': 'new_group_3'})

# 2-2. update a group where the test user does NOT belong
try:
    group_controller.update(group_admin_in_group_3_ret['access_token'], {'id': group_1_ret['id'], 'name': 'new_group_1'})
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex


### update
#  - Test user
#    - user

# 1. update the admin group
try:
    group_controller.update(user_in_group_1_ret['access_token'], {'id': ADMIN_GROUP_ID, 'name': 'new_admin'})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "You cannot update the admin group":
        pass
    else:
        raise ex

# 2-1. update a group where the test user belongs
try:
    group_controller.update(user_in_group_1_ret['access_token'], {'id': group_1_ret['id'], 'name': 'new_group_1'})
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2-2. update a group where the test user does NOT belong
try:
    group_controller.update(user_in_group_1_ret['access_token'], {'id': group_3_ret['id'], 'name': 'new_group_1'})
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex


####
# 'group_1_ret'
#   - user_in_group_1_ret as user
# 'group_2_ret'
#   - user_in_group_1_ret as admin
#   - group_admin_in_group_1_ret as user
#   - user_in_group_2_ret as user
# 'group_3_ret'
#   - group_admin_in_group_3_ret as admin

#########################################################################################################
# Delete a group
#########################################################################################################
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)

### delete
#  - Test user
#    - admin

# 1. delete the admin group
try:
    group_controller.delete(admin_token_ret['access_token'], {'id': ADMIN_GROUP_ID})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "You cannot remove the admin group":
        pass
    else:
        raise ex

# 2-1. delete a normal group that has users
try:
    group_controller.delete(admin_token_ret['access_token'], {'id': group_1_ret['id']})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "You must remove all users before removing this group":
        pass
    else:
        raise ex

# 2-2. delete a normal group that has NO users
## TODO:


### delete
#  - Test user
#    - group admin

# 1. delete the admin group
try:
    group_controller.delete(group_admin_in_group_3_ret['access_token'], {'id': ADMIN_GROUP_ID})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2-1. delete a group where the test user belongs and that has users
try:
    group_controller.delete(group_admin_in_group_3_ret['access_token'], {'id': group_3_ret['id']})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "You must remove all users before removing this group":
        pass
    else:
        raise ex

# 2-2. delete a group  where the test user belongs and that has NO users
## TODO:

# 2-3. delete a group where the test user does NOT belong and that has users
## TODO:

# 2-4. delete a group  where the test user does NOT belong and that has NO users
## TODO:


### delete
#  - Test user
#    - user

# 1. delete the admin group
try:
    group_controller.delete(user_in_group_3_ret['access_token'], {'id': ADMIN_GROUP_ID})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2-1. delete a group where the test user belongs and that has users
try:
    group_controller.delete(user_in_group_3_ret['access_token'], {'id': group_3_ret['id']})
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2-2. delete a group where the test user belongs and that has NO users
## TODO:

# 2-3. delete a group where the test user does NOT belong and that has users
## TODO:

# 2-4. delete a group  where the test user does NOT belong and that has NO users
## TODO:


#########################################################################################################

print("##########\nTest completed successfully")
