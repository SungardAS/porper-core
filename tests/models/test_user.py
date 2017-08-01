
import sys
sys.path.append('../../porper')

import boto3
dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

from models.user import User
user = User(dynamodb)

params = {'id': 'user1', 'email': 'user1@sungardas.com', 'family_name': 'family1', 'given_name': 'given1', 'name': 'given1 family1'}
user.create(params)
params = {'id': 'user2', 'email': 'user2@sungardas.com', 'family_name': 'family2', 'given_name': 'given2', 'name': 'given2 family2'}
user.create(params)

params = {'group_id': '1234'}
user.find(params)

params = {'group_ids': ['1234', 'abcd']}
user.find(params)

params = {'id': 'user1'}
user.find(params)

params = {'ids': ['user1', 'user2', 'userx']}
user.find(params)

params = {'email': 'user2@sungardas.com'}
user.find(params)
