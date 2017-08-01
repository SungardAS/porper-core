
import sys
sys.path.append('../../porper')

import boto3
dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

from models.permission import Permission
permission = Permission(dynamodb)

params = {'user_id': 'user1', 'action': 'action1', 'resource': 'res1', 'value': 'val1'}
permission.create(params)
params = {'user_id': 'user1', 'action': 'action2', 'resource': 'res2', 'value': '*'}
permission.create(params)
params = {'user_id': 'user2', 'action': 'action3', 'resource': 'res3', 'value': 'val3'}
permission.create(params)
params = {'user_id': 'user2', 'action': 'action4', 'resource': 'res4', 'value': '*'}
permission.create(params)

params = {'role_id': 'abcd', 'action': 'action11', 'resource': 'res11', 'value': 'val11'}
permission.create(params)
params = {'role_id': 'abcd', 'action': 'action12', 'resource': 'res12', 'value': '*'}
permission.create(params)
params = {'role_id': '1234', 'action': 'action13', 'resource': 'res13', 'value': 'val13'}
permission.create(params)
params = {'role_id': '1234', 'action': 'action14', 'resource': 'res14', 'value': '*'}
permission.create(params)

params = {'user_id': 'user1', 'action': 'actionx', 'resource': 'resx', 'value': 'valx'}
permission.create(params)
permission.delete(params)

params = {'role_id': '1234', 'action': 'actionx', 'resource': 'resx', 'value': 'valuex'}
permission.create(params)
permission.delete(params)

permission.delete({'id': '1234'})

params = {'action': 'action2', 'resource': 'res2', 'value': '*'}
permission.find(params)

params = {'user_id': 'user1', 'action': 'action1', 'resource': 'res1', 'value': 'val1'}
permission.find(params)

params = {'role_id': '1234', 'action': 'action13', 'resource': 'res13', 'value': 'val13'}
permission.find(params)

params = {'user_id': 'user2'}
permission.find(params)

params = {'role_id': 'abcd'}
permission.find(params)

params = {'user_id': 'user1', 'all':True}
permission.find(params)
