
import sys
sys.path.append('../../porper')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(dynamodb)

### are the permissions allowed?
params_list = [
  {
    'resource': 'account',
    'action': 'read',
    'value': '704579740447'
  },
  {
    'resource': 'service',
    #'action': 'read',
    'value': 'a990b2e1-bdf4-4435-b387-4f0ecfa96027',
    'parent': '704579740447'
    #'parent': '70457974044'   # to cause a failure in the parent permission check
  }
];
#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647'  # alex.ough's token
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'   # cloud_test_user's token
print permission_controller.are_permitted(access_token, params_list)


### 1. find all my permissions
#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647'  # alex.ough's token
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'   # cloud_test_user's token
params = {
  'resource': 'account'
  #'action': 'read'
}
print permission_controller.find_all(access_token, params)


### 2. find all permissions of given user if I'm the admin
#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647'  # alex.ough's token
#access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'   # cloud_test_user's token
access_token = '74a5a048-ab51-42a9-811f-a4cf82b72510'   # alex_group's token
params = {
  'resource': 'account',
  'action': 'read',
  #'user_id': 'c8b5dbbe-edd1-4e78-b03a-63b0d779be85' # alex_group
  'user_id': '49d8bc68-f57e-11e3-ba1d-005056ba0d15' # cloud_test_user
}
print permission_controller.find_all(access_token, params)


### 3. find all permissions of given group if I'm the admin
#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647'  # alex.ough's token
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'   # cloud_test_user's token
params = {
  resource: 'account',
  action: 'read',
  group_id: '3867c370-552f-43b8-bed9-6aa00ffc41b4'   # Awesome Group
};
print permission_controller.find_all(access_token, params)


# 4. find member's all permissions if I'm the group admin of the given group
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'    # cloud_test_user's token
#access_token = '74a5a048-ab51-42a9-811f-a4cf82b72510'   # alex_group's token
params = {
  resource: 'account',
  action: 'read',
  group_id: '3867c370-552f-43b8-bed9-6aa00ffc41b4'   # Awesome Group
}
print permission_controller.find_all(access_token, params)


### 5. find member's all permissions if I'm the group admin of any groups where the given user belongs
### 6. find member's all permissions if I'm the given user
#access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'    # cloud_test_user's token
access_token = '74a5a048-ab51-42a9-811f-a4cf82b72510'    # alex_group's token
params = {
  'resource': 'account',
  'action': 'read',
  'user_id': 'c8b5dbbe-edd1-4e78-b03a-63b0d779be85' # alex_group
};
print permission_controller.find_all(access_token, params)

connection.commit()
