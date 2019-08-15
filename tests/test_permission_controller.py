
import sys
sys.path.append("..")

import os
import boto3
region = os.environ.get('AWS_DEFAULT_REGION')
dynamodb = boto3.resource('dynamodb',region_name=region)

#########################################################################################################
# Preparation
#########################################################################################################

###### Find non-admin groups

# find all groups
from porper.models.group import Group
group = Group(dynamodb)
groups = group.find({})
group_ids = [g['id'] for g in groups]
role_ids = list(set([g['role_id'] for g in groups if 'role_id' in g]))

# find all roles
from porper.models.role import Role
role = Role(dynamodb)
roles = role.find_by_ids(role_ids)

# find non admin roles
ADMIN_FUNCTION_IDS = [
    "883b3842-35bb-4070-917f-a501e87bd695",
    "85af95c8-a6f5-4e14-9cf9-11bbced53255"
]
for r in roles:
    for f in r['functions']:
        if f in ADMIN_FUNCTION_IDS:
            r['is_admin'] = True
            break

non_admin_role_ids = [r['id'] for r in roles if r.get('is_admin') is None]

# now find non-admin groups
admin_group_ids = [g['id'] for g in groups if 'role_id' in g and g['role_id'] not in non_admin_role_ids]
#non_admin_group_ids = [g for g in group_ids if g not in admin_group_ids]

###### Find non-admin users
from porper.models.user_group import UserGroup
user_group = UserGroup(dynamodb)
admin_user_groups = user_group.find_by_group_ids(admin_group_ids)
admin_user_ids = [ug['user_id'] for ug in admin_user_groups]
all_user_groups = user_group.find({})
all_user_ids = [ug['user_id'] for ug in all_user_groups]
non_admin_user_ids = [u for u in all_user_ids if u not in admin_user_ids]

# finally non-admin groups & users
non_admin_user_group_ids = user_group.find_by_user_ids(non_admin_user_ids)

# fill customer ids
from porper.models.group import Group
group = Group(dynamodb)
for ug_id in non_admin_user_group_ids:
    ug_id['customer_id'] = group.find_by_id(ug_id['group_id'])['customer_id']


# non_admin_group_ids = [ug['group_id'] for ug in non_admin_user_group_ids]
#
# # group by customers
# from porper.models.group import Group
# group = Group(dynamodb)
# non_admin_groups = group.find_by_ids(non_admin_group_ids)
# non_admin_by_customer_id = {}
# for g in non_admin_groups:
#     if g['customer_id'] in non_admin_by_customer_id:
#         non_admin_by_customer_id[g['customer_id']][g['id']] = None
#     else:
#         non_admin_by_customer_id[g['customer_id']] = {g['id']: None}
#
# # fill users in groups by customer
# for g_ids in list(non_admin_by_customer_id.values()):
#     for g_id in list(g_ids.keys()):
#         g_ids[g_id] = [gu['user_id'] for gu in non_admin_user_group_ids if gu['group_id'] == group_id]
# for c_id in list(non_admin_by_customer_id.keys()):
#     print(c_id)
#     for g_id in list(non_admin_by_customer_id[c_id].keys()):
#         print(g_id)
#         non_admin_by_customer_id[c_id][g_id] = [gu['user_id'] for gu in non_admin_user_group_ids if gu['group_id'] == group_id]

#########################################################################################################
# Add permissions
#########################################################################################################

# find the access token of non-admin user
from porper.models.access_token import AccessToken
a = AccessToken(dynamodb)
user_access_token = None
# for c_id in list(non_admin_by_customer_id.keys()):
#     print(c_id)
#     for g_id in list(non_admin_by_customer_id[c_id].keys()):
#         print(g_id)
#         for u_id in non_admin_by_customer_id[c_id][g_id]:
#             print(u_id)
#             access_tokens = a.find({'user_id': u_id})
#             print(access_tokens)
#             if access_tokens:
#                 customer_id = c_id
#                 group_id = g_id
#                 owner_id = u_id
#                 user_access_token = access_tokens[0]['access_token']
#                 break
#         if user_access_token:
#             break
#     if user_access_token:
#         break
for ug_id in non_admin_user_group_ids:
    access_tokens = a.find({'user_id': ug_id['user_id']})
    if access_tokens:
        user_group_id = ug_id
        user_access_token = access_tokens[0]['access_token']
        break

# find groups of the selected user
from porper.models.user_group import UserGroup
user_group = UserGroup(dynamodb)
user_groups = user_group.find({'user_id': user_group_id['user_id']})

# now create permissions
from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(dynamodb)

# operations using admin user
params = {
    'owner_id': user_group_id['user_id'],
    'res_name': 'sla',
    'res_id': 'first',
    'permissions': [{'action': 'r'}, {'action': 'w'}],
    'to_group_ids': [user_group_id['group_id']]
}
permission_controller.create(user_access_token, params)

params = {
    #'action': 'r',
    'res_name': 'sla',
    #'res_id': resource_id
    #'value_only': True
}
ret = permission_controller.find(user_access_token, params)
print(ret)


##### need to work from here!!!!!!





# # operations using public user
# params = {
#     'owner_id': user_group_id['user_id'],
#     'resource_name': 'sla',
#     'resource_id': 'first',
#     'permissions': [{'action': 'r'}],
#     'to_group_ids': public_groups
# }
# permission_controller.create(public_access_token, params)
#
# params = {
#     'action': 'w',
#     'resource': 'sla',
#     #'value': resource_id,
#     'value_only': True
# }
# ret = permission_controller.find(public_access_token, params)
# print(ret)


#########################################################################################################
# GET by admin using PermissionController
#########################################################################################################

from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(dynamodb)

admin_access_token = '119d3da961a7f957d72627d7a2d2a5ed211ddbc6'

ret_all = permission_controller.find(admin_access_token, {})
print(len(ret_all))

ret_sla = permission_controller.find(admin_access_token, {'res_name': 'sla'})
print(len(ret_sla))

resource_id = ret_sla[0]['value']
ret_res = permission_controller.find(admin_access_token, {'res_name': 'sla', 'res_id': resource_id})
print(ret_res)

action = ret_res[0]['action']
ret_action = permission_controller.find(admin_access_token, {'res_name': 'sla', 'res_id': resource_id, 'action': action})
print(ret_action)


#########################################################################################################
# GET by group ids using Permission Model
#########################################################################################################

from porper.models.permission import Permission
permission = Permission(dynamodb)

user_id = ''
group_ids = list(set([i['group_id'] for i in ret_all]))
customer_id = ''

# search by all groups
search_params = {
    #'user_id': user_id,
    'group_ids': group_ids,
    #'customer_id': customer_id
}
p_ret_all = permission.find(search_params)
print(len(ret_all) == len(p_ret_all))

# search by all groups for 'sla'
search_params = {
    #'user_id': user_id,
    'group_ids': group_ids,
    #'customer_id': customer_id,
    'resource': 'sla'
}
p_ret_sla = permission.find(search_params)
print(len(ret_sla) == len(p_ret_sla))

# search by all groups for a specific 'sla' graph
search_params = {
    #'user_id': user_id,
    'group_ids': group_ids,
    #'customer_id': customer_id,
    'resource': 'sla',
    'value': resource_id
}
p_ret_res = permission.find(search_params)
print(len(ret_res) == len(p_ret_res))

# search by all groups for a specific 'sla' graph with a specific action
search_params = {
    #'user_id': user_id,
    'group_ids': group_ids,
    #'customer_id': customer_id,
    'resource': 'sla',
    'value': resource_id,
    'action': action
}
p_ret_action = permission.find(search_params)
print(len(ret_action) == len(p_ret_action))

# search with only 1 group
search_single_params = {
    #'user_id': user_id,
    'group_ids': group_ids[:1],
    #'customer_id': customer_id
}
p_ret_single = permission.find(search_single_params)
print(p_ret_single)

# ############### GET by user
#
# ## find access token of a user who
# # belongs 2 or more groups that has 'sla' graph access
# # and not super admin
#
# from porper.models.permission import Permission
# p = Permission(dynamodb)
# ret = p.find({})
# group_ids = [i['group_id'] for i in ret]
# group_ids = set(group_ids)
#
# from porper.models.user_group import UserGroup
# ug = UserGroup(dynamodb)
# user_groups = ug.find_by_group_ids(group_ids)
# user_ids = [ug['user_id'] for ug in user_groups]
# user_ids.sort()
#
# # find repeated user id and in non-super admin group
# user_id = ''
#
# from porper.models.access_token import AccessToken
# a = AccessToken(dynamodb)
# tokens = a.find({'user_id': user_id})
# user_access_token = tokens[0]['access_token']
#
# ## start testing
#
# ret = permission_controller.find(user_access_token, {'value_only': True})
# print(ret)
#
# ret = permission_controller.find(user_access_token, {'resource_name': 'sla'})
# print(ret)
#
# resource_id = ret[0]['value']
# ret = permission_controller.find(user_access_token, {'resource_name': 'sla', 'resource_id': resource_id})
# print(ret)
#
# action = ret[0]['action']
# ret = permission_controller.find(user_access_token, {'resource_name': 'sla', 'resource_id': resource_id, 'action': action})
# print(ret)
