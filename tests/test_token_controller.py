
import sys
sys.path.append("..")

import os
import boto3
region = os.environ.get('AWS_DEFAULT_REGION')
dynamodb = boto3.resource('dynamodb',region_name=region)

#########################################################################################################
# Preparation
# Find the access_token of an admin
#########################################################################################################

from porper.controllers.meta_resource_controller import ADMIN_GROUP_ID, PUBLIC_GROUP_ID

from util import find_token
admin_access_token = find_token(ADMIN_GROUP_ID)
public_access_token = find_token(PUBLIC_GROUP_ID)

from porper.controllers.token_controller import TokenController
token_controller = TokenController(dynamodb)

# find all access_tokens
ret = token_controller.find(admin_access_token, {})

# find this user's access_token
ret = token_controller.find(public_access_token, {})
