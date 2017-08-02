
import sys
sys.path.append('../../porper')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

from models.access_token import AccessToken
access_token = AccessToken(dynamodb)

params = {'access_token': '5550d59512546ad22951a56dd0a3b860739f9da0', 'refresh_token': '28769e2abdefab24c43d', 'refreshed_time': '2016-10-26 21:37:49', 'user_id': '35925'}
access_token.create(params)

params = {'access_token': '5550d59512546ad22951a56dd0a3b860739f9da0', 'refresh_token': '1111', 'refreshed_time': '2017-10-26 21:37:49'}
access_token.update(params)

params = {'access_token': '5550d59512546ad22951a56dd0a3b860739f9da0'}
access_token.find(params)
