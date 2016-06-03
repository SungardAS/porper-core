
from controllers.account_controller import AccountController
from controllers.permission_controller import PermissionController
from controllers.role_controller import RoleController
from controllers.service_controller import ServiceController
from controllers.access_token_controller import AccessTokenController
from controllers.user_controller import UserController
from controllers.user_role_controller import UserRoleController

ALLOWED_METHODS = [
    'create',
    'update',
    'delete',
    'find_all',
    'find_one'
]

ALLOWED_RESOURCES = [
    'account',
    'permission',
    'role',
    'service',
    'user',
    'user_role',
    'token'
]

def permission_handler(event, context):

    print event['region']
    print event['db']
    print event['oper']
    print event['params']

    oper = event.get('oper')
    if oper not in ALLOWED_METHODS: raise Exception("not supported method : %s" % oper)

    resource = event.get('resource')
    if resource not in ALLOWED_RESOURCES: raise Exception("not supported resource : %s" % resource)

    region = None
    connection = None
    if event.get('db') == 'mysql':
        from models.connection import connection
    else:
        region = event.get('region')

    params = event.get('params')
    access_token = event.get('access_token').replace("Bearer ", "")
    controller = globals()['%sController' % resource.title().replace('_', '')](region, connection)
    ret = getattr(controller, oper)(access_token, params)
    print ret
    return ret
    #if(connection)  connection.end()
