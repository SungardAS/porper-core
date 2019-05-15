
import sys
sys.path.append("..")

import os
import boto3
region = os.environ.get('AWS_DEFAULT_REGION')
dynamodb = boto3.resource('dynamodb',region_name=region)

def find_token(group_id):
    from porper.models.user_group import UserGroup
    from porper.models.access_token import AccessToken
    user_group_table = UserGroup(dynamodb)
    access_token_table = AccessToken(dynamodb)
    user_group_objs = user_group_table.find({"group_id": group_id})
    print(user_group_objs)
    for user_group_obj in user_group_objs:
        access_token_objs = access_token_table.find({'user_id': user_group_obj['user_id']})
        #print(access_token_objs)
        if access_token_objs:
            break
    return access_token_objs[0]['access_token']
