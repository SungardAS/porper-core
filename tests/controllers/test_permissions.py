
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


### Create 2 groups
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)
group_1 = {'name': 'group_1'}
group_1_ret = group_controller.create(admin_token_ret['access_token'], group_1)
group_2 = {'name': 'group_2'}
group_2_ret = group_controller.create(admin_token_ret['access_token'], group_2)


### Add a group admin and a user to each group

# invite a group admin
from porper.controllers.invited_user_controller import InvitedUserController
invited_user_controller = InvitedUserController(dynamodb)
invited_group_admin_in_group_1 = {
    "auth_type": "sso",
    "email": "group_1.admin@sungardas.com",
    "group_id": group_1_ret['id'],
    "is_admin": True
}
invited_group_admin_in_group_1_ret = invited_user_controller.create(admin_token_ret['access_token'], invited_group_admin_in_group_1)
invited_group_admin_in_group_2 = {
    "auth_type": "sso",
    "email": "group_2.admin@sungardas.com",
    "group_id": group_2_ret['id'],
    "is_admin": True
}
invited_group_admin_in_group_2_ret = invited_user_controller.create(admin_token_ret['access_token'], invited_group_admin_in_group_2)

# authenticate with the created group admin
from porper.controllers.auth_controller import AuthController
auth_controller = AuthController(dynamodb)
invited_group_admin_in_group_1_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': invited_group_admin_in_group_1_ret['email'],
    'family_name': "Group_1",
    'given_name': "Admin",
    'name': "Group2 Admin",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
group_admin_in_group_1_ret = auth_controller.authenticate(invited_group_admin_in_group_1_auth_params)
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

# invite a normal user
from porper.controllers.invited_user_controller import InvitedUserController
invited_user_controller = InvitedUserController(dynamodb)
invited_user_in_group_1 = {
    "auth_type": "sso",
    "email": "group_1.user@sungardas.com",
    "group_id": group_1_ret['id'],
    "is_admin": False
}
invited_user_in_group_1_ret = invited_user_controller.create(group_admin_in_group_1_ret['access_token'], invited_user_in_group_1)
invited_user_in_group_2 = {
    "auth_type": "sso",
    "email": "group_2.user@sungardas.com",
    "group_id": group_2_ret['id'],
    "is_admin": False
}
invited_user_in_group_2_ret = invited_user_controller.create(group_admin_in_group_2_ret['access_token'], invited_user_in_group_2)

# authenticate with the created normal user
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
invited_user_in_group_2_auth_params = {
    'user_id': str(uuid.uuid4()),
    'email': invited_user_in_group_2_ret['email'],
    'family_name': "Group_1",
    'given_name': "User",
    'name': "Group_1 User",
    'auth_type': 'sso',
    'access_token': str(uuid.uuid4()),
    'refresh_token': str(uuid.uuid4())
}
user_in_group_2_ret = auth_controller.authenticate(invited_user_in_group_2_auth_params)

print("admin_token_ret={}".format(admin_token_ret))
print("group_1_ret={}".format(group_1_ret))
print("group_2_ret={}".format(group_2_ret))
print("group_admin_in_group_1_ret={}".format(group_admin_in_group_1_ret))
print("group_admin_in_group_2_ret={}".format(group_admin_in_group_2_ret))
print("user_in_group_1_ret={}".format(user_in_group_1_ret))
print("user_in_group_2_ret={}".format(user_in_group_2_ret))


RESOURCE_NAME = 'aws_account'
RESOURCE_ACTION = ['add', 'remove', 'read', 'update']
#########################################################################################################
# Add permissions
#########################################################################################################
from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(dynamodb)

### add
#  - Test user
#    - admin

# 1. add 'add' & 'remove' permissions on the 'resource_01' to group_1
add_remove_on_resource_1_to_group_1_by_admin = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_01',
    'permissions':
    [
       {
           "action": "add"
       },
       {
           "action": "remove"
       }
    ],
    'to_group_id': group_1_ret['id']
}
permission_controller.create(admin_token_ret['access_token'], add_remove_on_resource_1_to_group_1_by_admin)

# 2. add 'read' & 'update' permissions on the 'resource_01' to user_1
read_update_on_resource_1_to_user_1_by_admin = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_01',
    'permissions':
    [
       {
           "action": "read"
       },
       {
           "action": "update"
       }
    ],
    'to_user_id': user_in_group_1_ret['user_id']
}
permission_controller.create(admin_token_ret['access_token'], read_update_on_resource_1_to_user_1_by_admin)

# 3. add 'read' permission on the 'resource_02' to group_2
read_on_resource_2_to_group_2_by_admin = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_02',
    'permissions':
    [
       {
           "action": "read"
       }
    ],
    'to_group_id': group_2_ret['id']
}
permission_controller.create(admin_token_ret['access_token'], read_on_resource_2_to_group_2_by_admin)

# 4. add all permissions on the 'resource_02' to user_2
all_on_resource_2_to_user_2_by_admin = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_02',
    'permissions':
    [
       {
           "action": permission_controller.PERMITTED_TO_ALL
       }
    ],
    'to_user_id': user_in_group_2_ret['user_id']
}
permission_controller.create(admin_token_ret['access_token'], all_on_resource_2_to_user_2_by_admin)

# 5. add 'read' permissions on the 'resource_03' to all users
read_on_resource_3_to_all_users_by_admin = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_03',
    'permissions':
    [
       {
           "action": "read"
       }
    ],
    'to_user_id': permission_controller.PERMITTED_TO_ALL
}
permission_controller.create(admin_token_ret['access_token'], read_on_resource_3_to_all_users_by_admin)

# 6. add 'update' permissions on the 'resource_03' to all groups
update_on_resource_3_to_all_groups_by_admin = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_03',
    'permissions':
    [
       {
           "action": "update"
       }
    ],
    'to_group_id': permission_controller.PERMITTED_TO_ALL
}
permission_controller.create(admin_token_ret['access_token'], update_on_resource_3_to_all_groups_by_admin)


### add
#  - Test user
#    - group admin

# 1. add 'add' permission on the 'resource_01' to a group_2
add_on_resource_1_to_group_2_by_group_admin = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_01',
    'permissions':
    [
       {
           "action": "add"
       }
    ],
    'to_group_id': group_2_ret['id']
}
try:
    permission_controller.create(group_admin_in_group_1_ret['access_token'], add_on_resource_1_to_group_2_by_group_admin)
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2. add 'read' permission on the 'resource_01' to a user_2
read_on_resource_1_to_user_2_by_group_admin = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_01',
    'permissions':
    [
       {
           "action": "read"
       }
    ],
    'to_user_id': user_in_group_2_ret['user_id']
}
try:
    permission_controller.create(group_admin_in_group_1_ret['access_token'], read_on_resource_1_to_user_2_by_group_admin)
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex


### add
#  - Test user
#    - user

# 1. add 'add' permission on the 'resource_01' to a group_2
add_on_resource_1_to_group_2_by_user = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_01',
    'permissions':
    [
       {
           "action": "add"
       }
    ],
    'to_group_id': group_2_ret['id']
}
try:
    permission_controller.create(user_in_group_1_ret['access_token'], add_on_resource_1_to_group_2_by_user)
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex

# 2. add 'read' permission on the 'resource_01' to a user_2
read_on_resource_1_to_user_2_by_user = {
    'resource_name': RESOURCE_NAME,
    'resource_id': 'resource_01',
    'permissions':
    [
       {
           "action": "read"
       }
    ],
    'to_user_id': user_in_group_2_ret['user_id']
}
try:
    permission_controller.create(user_in_group_1_ret['access_token'], read_on_resource_1_to_user_2_by_user)
    raise Exception("should be failed")
except Exception as ex:
    print(ex)
    if str(ex) == "not permitted":
        pass
    else:
        raise ex


"""
admin_token_ret={'access_token': 'b4d7adb4-aaef-4b81-9a72-5560453321aa', 'user_id': 'd4c68663-628c-41f9-8f5f-dcfed95b5106', 'refreshed_time': '2018-06-17 16:19:55.343193', 'refresh_token': 'd3d49ae3-8948-4bad-aae6-29013a554cd2', 'time_stamp': '1529270395'}
group_1_ret={'name': 'group_1', 'id': 'f00f060a-ab7a-4034-8e5a-414865bb3a9f'}
group_2_ret={'name': 'group_2', 'id': 'f0176e89-f7a0-4f58-8330-74aa87fd0f84'}
group_admin_in_group_1_ret={'access_token': '77f285b9-726c-4d8b-b7e7-15ad3a5c5184', 'user_id': 'b06de2ba-e61d-4f17-b4f2-df6700dc32e4', 'refreshed_time': '2018-06-17 21:19:56.751199', 'refresh_token': '2ee9a49b-becd-4541-a411-3de3433c1a80', 'time_stamp': '1529288396'}
group_admin_in_group_2_ret={'access_token': '6ba939cc-1e6a-45d3-875e-c5dec7d9d43d', 'user_id': '79e7353f-8e87-49a1-8099-c30d5b4b2f22', 'refreshed_time': '2018-06-17 21:19:57.460484', 'refresh_token': 'bc2d681b-7a7d-435e-84a2-9a57bcc51584', 'time_stamp': '1529288397'}
user_in_group_1_ret={'access_token': 'f4640fec-15bf-43f5-b7c3-b735491537b4', 'user_id': 'b510c186-2342-48cc-a45a-ae4429e59d6e', 'refreshed_time': '2018-06-17 21:19:58.699249', 'refresh_token': '8c101a12-aad7-435a-87cc-25927828d994', 'time_stamp': '1529288398'}
user_in_group_2_ret={'access_token': 'd7193bc7-7451-4ecd-a7c4-777dc7f0eb73', 'user_id': '668b9760-386d-40c3-8512-7d0b311d1384', 'refreshed_time': '2018-06-17 21:19:59.508951', 'refresh_token': 'da7a862b-3c7e-43ac-91a4-127bc500c344', 'time_stamp': '1529288399'}
"""

####
# 'group_1_ret'
#   - 'add' & 'remove' on 'resource_01'
# 'group_2_ret'
#   - 'read' on 'resource_02'
# all groups
#   - 'update' on 'resource_03'

# 'user_in_group_1_ret'
#   - 'read' & 'update' on 'resource_01'
# 'user_in_group_2_ret'
#   - '*' on 'resource_02'
# all users
#   - 'read' on 'resource_03'
#########################################################################################################
# Find permissions
#########################################################################################################
from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(dynamodb)

### add
#  - Test user
#    - admin

# 1. Find all permissions
num_of_perms = 8
permissions = permission_controller.find(admin_token_ret['access_token'], None)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 2-1. Find all permissions to 'group_1_ret'
num_of_perms = 3
params = {
    'group_id': group_1_ret['id']
}
permissions = permission_controller.find(admin_token_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 2-2. Find all permissions to 'group_2_ret'
num_of_perms = 2
params = {
    'group_id': group_2_ret['id']
}
permissions = permission_controller.find(admin_token_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 2-3. Find all permissions to all groups
num_of_perms = 1
params = {
    'group_id': permission_controller.PERMITTED_TO_ALL
}
permissions = permission_controller.find(admin_token_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 3-1. Find all permissions to 'user_in_group_1_ret'
num_of_perms = 6
params = {
    'user_id': user_in_group_1_ret['user_id']
}
permissions = permission_controller.find(admin_token_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 3-2. Find all permissions to 'user_in_group_2_ret'
num_of_perms = 4
params = {
    'user_id': user_in_group_2_ret['user_id']
}
permissions = permission_controller.find(admin_token_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 3-3. Find all permissions to all users
num_of_perms = 2
params = {
    'user_id': permission_controller.PERMITTED_TO_ALL
}
permissions = permission_controller.find(admin_token_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))





### add
#  - Test user
#    - user

# 1. Find all permissions
num_of_perms = 6
permissions = permission_controller.find(user_in_group_1_ret['access_token'], None)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 2-1. Find all permissions to 'group_1_ret'
num_of_perms = 3
params = {
    'group_id': group_1_ret['id']
}
permissions = permission_controller.find(user_in_group_1_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 2-2. Find all permissions to 'group_2_ret'
num_of_perms = 0
params = {
    'group_id': group_2_ret['id']
}
permissions = permission_controller.find(user_in_group_1_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 2-3. Find all permissions to all groups
num_of_perms = 0
params = {
    'group_id': permission_controller.PERMITTED_TO_ALL
}
permissions = permission_controller.find(user_in_group_1_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 3-1. Find all permissions to 'user_in_group_1_ret'
num_of_perms = 6
params = {
    'user_id': user_in_group_1_ret['user_id']
}
permissions = permission_controller.find(user_in_group_1_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 3-2. Find all permissions to 'user_in_group_2_ret'
num_of_perms = 0
params = {
    'user_id': user_in_group_2_ret['user_id']
}
permissions = permission_controller.find(user_in_group_1_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))

# 3-3. Find all permissions to all users
num_of_perms = 0
params = {
    'user_id': permission_controller.PERMITTED_TO_ALL
}
permissions = permission_controller.find(user_in_group_1_ret['access_token'], params)
print("there are {} permissions".format(len(permissions)))
if len(permissions) != num_of_perms:
    raise Exception("number of permissions should be {}".format(num_of_perms))




"""
#########################################################################################################
# Update permissions
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




#########################################################################################################
# Remove permissions
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
"""

#########################################################################################################

print("##########\nTest completed successfully")
