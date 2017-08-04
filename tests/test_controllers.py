
import sys
sys.path.append('..')

import os
region = os.environ.get('AWS_DEFAULT_REGION')

import boto3
dynamodb = boto3.resource('dynamodb',region_name=region)

# read input json
from input_local import INPUT

print "\n\n\n##############################################################################"
print "# User Auth"
print "##############################################################################"
print "\n# create an admin user using a google user"
if INPUT['google']['id_token']:
    from porper.controllers.google_auth_controller import GoogleAuthController
    google_auth_controller = GoogleAuthController(dynamodb)
    ret = google_auth_controller.authenticate(INPUT['google'])
    google_access_token = ret['access_token']
else:
    from porper.controllers.auth_controller import AuthController
    auth_controller = AuthController(dynamodb)
    ret = auth_controller.authenticate('google_user_1', 'user1@google.com', 'google', 'user', 'Google User', 'google', 'google_access_token', 'google_refresh_token')
    google_access_token = 'google_access_token'

print "\n# create another user using github user"
if INPUT['github']['code']:
    from porper.controllers.github_auth_controller import GithubAuthController
    github_auth_controller = GithubAuthController(dynamodb)
    ret = github_auth_controller.authenticate(INPUT['github'])
    github_access_token = ret['access_token']
else:
    from porper.controllers.auth_controller import AuthController
    auth_controller = AuthController(dynamodb)
    ret = auth_controller.authenticate('github_user_1', 'user1@github.com', 'github', 'user', 'Github User', 'github', 'github_access_token', 'github_refresh_token')
    github_access_token = 'github_access_token'

print "\n# create the third user using dummy info"
from porper.controllers.auth_controller import AuthController
auth_controller = AuthController(dynamodb)
ret = auth_controller.authenticate('user_id', 'email', 'family_name', 'given_name', 'name', 'dummy', 'access_token', 'refresh_token')
dummy_access_token = 'access_token'

print "\n\n\n##############################################################################"
print "# Group"
print "##############################################################################"
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)

print "\n\n#### admin (google user)"
print "\n#find public group"
items1 = group_controller.find(google_access_token, {'name': 'public'})
ret = items1[0]['name'] == 'public'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n# list all groups as admin (google user)"
items2 = group_controller.find(google_access_token, {})
ret = len(items2) == 2
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n# find a group with the ids"
ids = [ item['id'] for item in items2 ]
items3 = group_controller.find(google_access_token, {'id': ids[0]})
ret = items3[0]['id'] == ids[0]
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

items4 = group_controller.find(google_access_token, {'ids': ids})
ret = len(items4) == 2
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n\n#### normal user (github user)"
print "\n# try creating a group"
try:
    group_controller.create(github_access_token, "should be failed")
    print "FAILED!!!!!!!!"
    sys.exit()
except:
    print True

print "\n# list groups"
items5 = group_controller.find(github_access_token, {})
ret = len(items5) == 0
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()


print "\n\n\n##############################################################################"
print "# UserGroup"
print "##############################################################################"
from porper.controllers.user_controller import UserController
user_controller = UserController(dynamodb)
from porper.controllers.group_controller import GroupController
group_controller = GroupController(dynamodb)

print "\n\n#### admin (google user)"
print "\n# find user_id of google user"
users = user_controller.find(google_access_token, {'auth_type': 'google'})
ret = len(users) == 1 and users[0]['auth_type'] == 'google'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()
google_user_id = users[0]['id']

print "\n# find user_id of github user"
users = user_controller.find(google_access_token, {'auth_type': 'github'})
ret = len(users) == 1 and users[0]['auth_type'] == 'github'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()
github_user_id = users[0]['id']

print "\n# find user_id of dummy user"
users = user_controller.find(google_access_token, {'auth_type': 'dummy'})
ret = len(users) == 1 and users[0]['auth_type'] == 'dummy'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()
dummy_user_id = users[0]['id']

print "\n# find groups"
all_groups = group_controller.find(google_access_token, {})
admin_group_id = [ group for group in all_groups if group['name'] == 'admin'][0]['id']
print admin_group_id
public_group_id = [ group for group in all_groups if group['name'] == 'public'][0]['id']
print public_group_id

print "\n# add github user to public group as admin"
ret = user_controller.create(google_access_token, {'user_id': github_user_id, 'group_id': public_group_id, 'is_admin': True})
print ret

print "\n# add dummy user to public group as user"
ret = user_controller.create(google_access_token, {'user_id': dummy_user_id, 'group_id': public_group_id, 'is_admin': False})
print ret

print "\n# find all groups of google user"
google_groups = group_controller.find(google_access_token, {'user_id': google_user_id})
ret = len(google_groups) == 1 and google_groups[0]['name'] == 'admin'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n# find all groups of google user"
github_groups = group_controller.find(google_access_token, {'user_id': github_user_id})
ret = len(github_groups) == 1 and github_groups[0]['name'] == 'public'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n# find all users of admin group"
admin_users = user_controller.find(google_access_token, {'group_id': admin_group_id})
ret = len(admin_users) == 1 and admin_users[0]['auth_type'] == 'google'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n# find all users of public group"
public_users = user_controller.find(google_access_token, {'group_id': public_group_id})
ret = len(public_users) == 2 and 'github' in [ public_user['auth_type'] for public_user in public_users ] and 'dummy' in [ public_user['auth_type'] for public_user in public_users ]
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()


print "\n\n#### group admin (github user)"
print "\n# find all groups of google user"
google_groups = group_controller.find(github_access_token, {'user_id': google_user_id})
ret = len(google_groups) == 0
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n# find all groups of google user"
github_groups = group_controller.find(github_access_token, {'user_id': github_user_id})
ret = len(github_groups) == 1 and github_groups[0]['name'] == 'public'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

github_groups = group_controller.find(github_access_token, {})
ret = len(github_groups) == 1 and github_groups[0]['name'] == 'public'
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n# find all users of admin group"
admin_users = user_controller.find(github_access_token, {'group_id': admin_group_id})
ret = len(admin_users) == 0
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n# find all users of public group"
public_users = user_controller.find(github_access_token, {'group_id': public_group_id})
ret = len(public_users) == 2 and 'github' in [ public_user['auth_type'] for public_user in public_users ] and 'dummy' in [ public_user['auth_type'] for public_user in public_users ]
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

public_users = user_controller.find(github_access_token, {})
ret = len(public_users) == 2 and 'github' in [ public_user['auth_type'] for public_user in public_users ] and 'dummy' in [ public_user['auth_type'] for public_user in public_users ]
if not ret:
    print "FAILED!!!!!!!!"
    sys.exit()

print "\n\n\nCOMPLETED!!!!"
