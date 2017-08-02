
import sys
sys.path.append('../../porper')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

from models.user_group import UserGroup
ur = UserGroup(dynamodb)

params = {'user_id':'user1', 'group_id':'abcd', 'is_admin':True}
ur.create(params)
params = {'user_id':'user1', 'group_id':'1234', 'is_admin':False}
ur.create(params)
params = {'user_id':'user2', 'group_id':'abcd', 'is_admin':False}
ur.create(params)
params = {'user_id':'user2', 'group_id':'1234', 'is_admin':True}
ur.create(params)

params = {'user_id':'user1', 'group_id':'abcd'}
ur.find(params)
params = {'user_id':'user1'}
ur.find(params)
params = {'group_id':'abcd'}
ur.find(params)

params = {'user_id':'userx', 'group_id':'groupx', 'is_admin':True}
ur.create(params)
params = {'user_id':'userx', 'group_id':'groupx'}
ur.delete(params)
