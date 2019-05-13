
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
from util import find_admin_token
admin_access_token = find_admin_token()


### Create a group
from porper.controllers.cognito_auth_controller import CognitoAuthController
cognito_auth_controller = CognitoAuthController(dynamodb)

cognito_access_token = ""
params = {"access_token": admin_access_token, "cognito_access_token": cognito_access_token}
cognito_auth_controller.authenticate(params)
