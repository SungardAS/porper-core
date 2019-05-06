
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


from porper.controllers.function_controller import FunctionController
function_controller = FunctionController(dynamodb)
functions = function_controller.find(admin_access_token, {})


### Create a role
from porper.controllers.role_controller import RoleController
role_controller = RoleController(dynamodb)

role_obj = {'name': 'role_1', 'functions': [functions[0]["id"]]}
ret_1 = role_controller.create(admin_access_token, role_obj)
# {'name': 'role_1', 'functions': ['8c146935-47d5-4dd2-bc3a-74c5604c0c55'], 'id': '0f15f72c-4f54-4872-91d8-ce6f8dc43af8'}

role_obj = {'name': 'role_2', 'functions': [functions[0]["id"], functions[1]["id"]]}
ret_2 = role_controller.create(admin_access_token, role_obj)
# {'name': 'role_2', 'functions': ['8c146935-47d5-4dd2-bc3a-74c5604c0c55', 'f3542ad2-31b3-41f4-bf52-ad09643aac93'], 'id': 'd5ccb254-1aa2-44a0-85a7-4d07c1d25c4e'}

## Find roles
roles = role_controller.find(admin_access_token, {})

role = role_controller.find(admin_access_token, {"id": ret_2["id"]})


### Update a role
ret_1['name'] = "role_1_new"
ret_1['functions'] = [functions[0]["id"], functions[1]["id"]]
updated = role_controller.update(admin_access_token, ret_1)
role = role_controller.find(admin_access_token, {"id": ret_1["id"]})


### Delete a role
role_controller.delete(admin_access_token, {"id": ret_1["id"]})

roles = role_controller.find(admin_access_token, {})
