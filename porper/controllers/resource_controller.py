
ALL = "*"

class ResourceController():

    def __init__(self, account_id, region, permission_connection):
        self.account_id = account_id
        self.region = region
        self.connection = permission_connection
        self.resource = None
        self.model = None
        from porper.controllers.permission_controller import PermissionController
        self.permission_controller = PermissionController(self.connection)

    @property
    def model_name(self):
        return self.model.__class__.__name__

    def add_permissions(self, id, user_id, user_actions, group_id, group_actions):
        if user_id and user_actions:
            # add update/delete permissions to this user
            user_permission_params = {
                "user_id": user_id,
                "resource": self.resource,
                "value": id,
                "action": None
            }
            for action in user_actions:
                user_permission_params["action"] = action
                permission_controller.create(None, user_permission_params, user_id)
        if group_id and group_actions:
            # add read permission to the given group
            group_permission_params = {
                "group_id": group_id,
                "resource": self.resource,
                "value": id,
                "action": None
            }
            for action in group_actions:
                group_permission_params["action"] = action
                ###group_permission_params["condition"] = json.dumps({"is_admin": 1})
                permission_controller.create(None, group_permission_params, user_id)

    def _find_permitted(self, access_token, action, id=None):
        params = {
            'action': action,
            'resource': self.resource,
            'all': True
        }
        if id: params['value'] = id
        permissions = self.permission_controller.find_all(access_token, params)
        print 'permissions : %s' % permissions
        return permissions

    def is_permitted(self, access_token, action, id):
        #permissions = self._find_permitted(access_token, action, id)
        #return len(permissions) > 0
        params = {
            'action': action,
            'resource': self.resource,
            'all': True,
            'value': id
        }
        return self.permission_controller.is_permitted(access_token, params)

    def create(self, access_token, params):
        if not self.is_permitted(access_token, 'create', params['id']):    raise Exception("not permitted")
        ret = self.model.create(params)
        print "%s is successfully created : %s" % (self.model_name, ret)
        return ret

    def update(self, access_token, params):
        if not self.is_permitted(access_token, 'update', params['id']):    raise Exception("not permitted")
        ret = self.model.update(params)
        print "%s [%s] is successfully updated : %s" % (self.model_name, params['id'], ret)
        return ret

    def delete(self, access_token, params):
        if not self.is_permitted(access_token, 'delete', params['id']):    raise Exception("not permitted")
        ret = self.model.delete(params['id'])
        print "%s [%s] is successfully deleted : %s" % (self.model_name, params['id'], ret)
        return ret

    # find all read-permitted instances of the current resource, so 'id' is NOT given
    def find(self, access_token, params):
        permissions = self._find_permitted(access_token, 'read')
        if len(permissions) == 0:   raise Exception("not permitted")
        ids = [ permission['value'] for permission in permissions ]
        if params is None:
            if ALL not in ids:
                return self.model.find_by_ids(ids)
            else:
                return self.model.find()
        elif params.get('id'):
            if ALL in ids or params['id'] in ids:
                return self.model.find_by_id(params['id'])
            else:
                return []
        else:
            return self.model.find(params)

    # find one read-permitted instance of the current resource whose id is the given
    def find_by_id(self, access_token, id):
        permissions = self._find_permitted(access_token, 'read', params['id'])
        if len(permissions) == 0:   raise Exception("not permitted")
        for permission in permissions:
            if permission['value'] == params['id'] or permission['value'] == ALL:
                return self.model.find_by_id(params['id'])
        return None
