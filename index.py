
from controllers.permission_controller import PermissionController
from controllers.role_controller import RoleController
from controllers.token_controller import TokenController
from controllers.user_controller import UserController
from controllers.user_role_controller import UserRoleController
from controllers.invited_user_controller import InvitedUserController

ALLOWED_METHODS = [
    'create',
    'update',
    'delete',
    'find_all',
    'find_one'
]

ALLOWED_RESOURCES = [
    'permission',
    'role',
    'user',
    'user_role',
    'token',
    'invited_user'
]

def permission_handler(event, context):

    print event['oper']
    print event['params']

    oper = event.get('oper')
    if oper not in ALLOWED_METHODS: raise Exception("not supported method : %s" % oper)

    resource = event.get('resource')
    if resource not in ALLOWED_RESOURCES: raise Exception("not supported resource : %s" % resource)

    try:
        from models.connection import connection
        print connection

        params = event.get('params')
        access_token = event.get('access_token').replace("Bearer ", "")
        controller = globals()['%sController' % resource.title().replace('_', '')](connection)
        ret = getattr(controller, oper)(access_token, params)
        connection.commit()
        print ret
        return ret
    except Exception, ex:
        print ex
        if connection:  connection.rollback()
        raise ex


def connection_handler(event, context):
    try:
        import json
        # don't overwrite if the info is already populated
        with open('models/config.json') as data_file:
            connection_info = json.load(data_file)
            if connection_info['host']:
                raise Exception('already populated')
        if not event['host']:
            raise Exception('host is not given')
        if not event['database']:
            raise Exception('database is not given')
        if not event['username']:
            raise Exception('username is not given')
        if not event['password']:
            raise Exception('password is not given')
        f = open('models/config.json', 'w')
        f.write(json.dumps(event))
        f.close()
        return True
    except Exception, ex:
        print ex
        raise ex
