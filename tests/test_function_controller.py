
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


### Create a function
from porper.controllers.function_controller import FunctionController
function_controller = FunctionController(dynamodb)

permissions_all = [
    {"resource_name": "sla", "permissions": "rw"},
    {"resource_name": "meta", "permissions": "rw"},
]
permissions_view_meta = [
    {"resource_name": "sla", "permissions": "rw"},
    {"resource_name": "meta", "permissions": "r"},
]
permissions_only_sla = [
    {"resource_name": "sla", "permissions": "rw"}
]

function_obj = {'name': 'function_1', 'permissions': permissions_all}
ret_1 = function_controller.create(admin_access_token, function_obj)
# {'name': 'function_1', 'permissions': [{'resource_name': 'sla', 'permissions': 'rw'}, {'resource_name': 'meta', 'permissions': 'rw'}], 'id': '8c146935-47d5-4dd2-bc3a-74c5604c0c55'}

function_obj = {'name': 'function_2', 'permissions': permissions_view_meta}
ret_2 = function_controller.create(admin_access_token, function_obj)
# {'name': 'function_2', 'permissions': [{'resource_name': 'sla', 'permissions': 'rw'}, {'resource_name': 'meta', 'permissions': 'r'}], 'id': '146fa992-6272-41e0-b4db-7c4bcfa70392'}

function_obj = {'name': 'function_3', 'permissions': permissions_only_sla}
ret_3 = function_controller.create(admin_access_token, function_obj)
# {'name': 'function_3', 'permissions': [{'resource_name': 'sla', 'permissions': 'rw'}], 'id': 'f3542ad2-31b3-41f4-bf52-ad09643aac93'}

## Find functions
functions = function_controller.find(admin_access_token, {})

function = function_controller.find(admin_access_token, {"id": ret_2["id"]})


### Update a function
ret_3['name'] = "meta view and sla all"
ret_3['permissions'] = permissions_view_meta
updated = function_controller.update(admin_access_token, ret_3)
function = function_controller.find(admin_access_token, {"id": ret_3["id"]})


### Delete a function
function_controller.delete(admin_access_token, {"id": ret_2["id"]})

functions = function_controller.find(admin_access_token, {})
