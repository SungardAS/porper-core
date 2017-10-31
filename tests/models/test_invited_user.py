
import sys
sys.path.append('../../porper')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

from models.invited_user import InvitedUser
invited_user = InvitedUser(dynamodb)

params = {'email': 'invited1@sungardas.com', 'role_id': '1a714ec0-5132-4749-8f51-be30f6e393f3', 'invited_by': 'user1', 'invited_at': '2016-10-26 21:56:11', 'state': 'a', 'is_admin': True}
invited_user.create(params)
params = {'email': 'invited2@sungardas.com', 'role_id': '1a714ec0-5132-4749-8f51-be30f6e393f3', 'invited_by': 'user2', 'invited_at': '2016-10-26 21:56:11', 'state': 'a', 'is_admin': False}
invited_user.create(params)
params = {'email': 'invited3@sungardas.com', 'role_id': '1234', 'invited_by': 'user1', 'invited_at': '2016-10-26 21:56:11', 'state': 'a', 'is_admin': False}
invited_user.create(params)
params = {'email': 'invited4@sungardas.com', 'role_id': '1234', 'invited_by': 'user2', 'invited_at': '2016-10-26 21:56:11', 'state': 'a', 'is_admin': True}
invited_user.create(params)

params = {'email': 'invited3@sungardas.com', 'state':'b'}
invited_user.update(params)

params = {'email': 'invited4@sungardas.com', 'state':'b'}
invited_user.find(params)

params = {'role_id': '1234'}
invited_user.find(params)

params = {'role_ids': ['1234', '1a714ec0-5132-4749-8f51-be30f6e393f3']}
invited_user.find(params)
