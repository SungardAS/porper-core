
import json
import sys
sys.path.append("..")

import os
import boto3
region = os.environ.get('AWS_DEFAULT_REGION')
dynamodb = boto3.resource('dynamodb',region_name=region)

from porper.models.user_group import UserGroup
obj = UserGroup(dynamodb)
ret = obj.find({})
file = open('../data/migration/user_group.json', 'w')
file.write(json.dumps(ret))
file.close()



### AccessToken
from porper.models.access_token import AccessToken
obj = AccessToken(dynamodb)
#ret = obj.find({})
items = []
last_evaluated_key = None
while True:
    if last_evaluated_key:
        ret = obj.table.scan(ExclusiveStartKey=last_evaluated_key)
    else:
        ret = obj.table.scan()
    print(ret['Items'])
    items = items + ret['Items']
    last_evaluated_key = ret.get("LastEvaluatedKey")
    if last_evaluated_key is None:
        break

file = open('../data/migration/access_token.json', 'w')
file.write(json.dumps(items))
file.close()

import uuid
sql = "INSERT INTO Token(id,user_id,access_token,refresh_token,refreshed_time) VALUES ('{}','{}','{}','{}','{}');"
sqls = []
for item in ret:
    sqls.append(sql.format(str(uuid.uuid4()), item['user_id'], item['access_token'], item['refresh_token'], item['refreshed_time']))

file = open('../data/migration/access_token.sql', 'w')
file.write("\n".join(sqls))
file.close()



### InvitedUser
from porper.models.invited_user import InvitedUser
obj = InvitedUser(dynamodb)
ret = obj.find({})
file = open('../data/migration/invited_user.json', 'w')
file.write(json.dumps(ret))
file.close()

import uuid
sql = "INSERT INTO InvitedUser(id,invited_by,email,invited_at,auth_type,group_id,state) VALUES ('{}','{}','{}','{}','{}','{}','{}');"
sqls = []
for item in ret:
    sqls.append(sql.format(str(uuid.uuid4()), item['invited_by'], item['email'], item['invited_at'], item['auth_type'], item['group_id'], item['state']))

file = open('../data/migration/invited_user.sql', 'w')
file.write("\n".join(sqls))
file.close()



### UserGroup
from porper.models.user_group import UserGroup
obj = UserGroup(dynamodb)
ret = obj.find({})
file = open('../data/migration/user_group.json', 'w')
file.write(json.dumps(ret))
file.close()

import uuid
sql = "INSERT INTO Group_User(id,user_id,group_id) VALUES ('{}','{}','{}');"
sqls = []
for item in ret:
    sqls.append(sql.format(str(uuid.uuid4()), item['user_id'], item['group_id']))

file = open('../data/migration/user_group.sql', 'w')
file.write("\n".join(sqls))
file.close()



### FunctionPermission
from porper.models.function import Function
obj = Function(dynamodb)
ret = obj.find({})
file = open('../data/migration/function.json', 'w')
file.write(json.dumps(ret))
file.close()

import uuid
sql_perm = "INSERT INTO Permission(id,res_name,action) VALUES ('{}','{}','{}');"
sql = "INSERT INTO Function_Permission(id,function_id,permission_id) VALUES ('{}','{}','{}');"
permission_dict = {}
sql_perms = []
sqls = []
for item in ret:
    for permission in item['permissions']:
        key = "{}.{}".format(permission['resource'], permission['action'])
        perm_uuid = permission_dict.get(key)
        if perm_uuid is None:
            perm_uuid = str(uuid.uuid4())
            sql_perms.append(sql_perm.format(perm_uuid, permission['resource'], permission['action']))
            permission_dict[key] = perm_uuid
        sqls.append(sql.format(str(uuid.uuid4()), item['id'], perm_uuid))

file = open('../data/migration/function_permission.sql', 'w')
file.write("\n".join(sql_perms))
file.write("\n")
file.write("\n".join(sqls))
file.close()



### RoleFunction
from porper.models.role import Role
obj = Role(dynamodb)
ret = obj.find({})
file = open('../data/migration/role.json', 'w')
file.write(json.dumps(ret))
file.close()

import uuid
sql = "INSERT INTO Role_Function(id,role_id,function_id) VALUES ('{}','{}','{}');"
sqls = []
for item in ret:
    for function in item['functions']:
        sqls.append(sql.format(str(uuid.uuid4()), item['id'], function))

file = open('../data/migration/role_function.sql', 'w')
file.write("\n".join(sqls))
file.close()
