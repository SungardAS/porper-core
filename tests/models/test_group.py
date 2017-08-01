
import sys
sys.path.append('../../porper')

import boto3
dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

from models.group import Group
group = Group(dynamodb)

params = {'name': 'public'}
group.create(params)
params = {'id': '1234', 'name': 'new'}
group.create(params)
params = {'id': 'abcd', 'name': 'old'}
group.create(params)

params = {'id': '1234'}
group.find(params)

params = {'ids': ['1234', 'tt']}
group.find(params)

params = {}
group.find(params)
