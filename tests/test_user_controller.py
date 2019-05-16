
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
#from util import find_admin_token
#admin_access_token = find_admin_token()

from porper.controllers.token_controller import TokenController
token_controller = TokenController(dynamodb)

from porper.controllers.user_controller import UserController
user_controller = UserController(dynamodb)

for token in token_controller.find({}):
    #user = user_controller.find_detail(token['access_token'], {})
    user = user_controller.find(token['access_token'], {'detail': True})
    print(user)
    print("\n\n")


for token in token_controller.find({}):
    #user = user_controller.find_detail(token['access_token'], {})
    user = user_controller.find(token['access_token'], {})
    print(user)
    print("\n\n")


user = user_controller.find(token['access_token'], {"id": 'ac563dca-2069-4ffd-8ed5-b898a70406d0'})
