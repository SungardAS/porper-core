
import json
from porper.controllers.meta_resource_controller import MetaResourceController

class PermissionController(MetaResourceController):

    def __init__(self, connection=None):
        MetaResourceController.__init__(self, connection)
        from porper.models.permission import Permission
        from porper.models.user_group import UserGroup
        self.permission = Permission(self.connection)
        self.user_group = UserGroup(self.connection)
        from porper.models.user import User
        from porper.models.group import Group
        self.user = User(self.connection)
        self.group = Group(self.connection)
        from porper.models.access_token import AccessToken
        self.access_token = AccessToken(self.connection)
        # from porper.controllers.token_controller import TokenController
        # self.token_controller = TokenController(self.connection)
        # from porper.controllers.user_group_controller import UserGroupController
        # self.user_group_controller = UserGroupController(self.connection)

        from porper.models.permission import ALL
        self.PERMITTED_TO_ALL = ALL



    # def is_admin(self, user_id):
    #     return self.user_group_controller.is_admin(user_id)
    #
    # def is_group_admin(self, user_id, group_id):
    #     return self.user_group_controller.is_group_admin(user_id, group_id)
    #
    # def is_member(self, user_id, group_id):
    #     return self.user_group_controller.is_member(user_id, group_id)
    #
    # def is_permitted(self, access_token, params):
    #     """
    #     possible attributes in params
    #         - None
    #         - [user_id | group_id], action, resource, value
    #     """
    #     current_user_id = self.token_controller.find_user_id(access_token)
    #     if self.is_admin(current_user_id):    return True
    #
    #     #params['all'] = True
    #     rows = self.find(access_token, params)
    #     print("permitted : {}".format(rows))
    #     if len(rows) == 0:  return False
    #     return True

    def find_user_id(self, access_token):
        params = {
            'access_token': access_token
        }
        return self.access_token.find(params)[0]['user_id']


    def add_permissions_to_group(self, resource_name, resource_id, permissions, to_group_id):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        group_permission_params = {
            "group_id": to_group_id,
            "resource": resource_name,
            "value": resource_id
        }
        for permission in permissions:
            group_permission_params["action"] = permission['action']
            if permission.get('condition'):
                group_permission_params['condition'] = permission['condition']
            self.permission.create(group_permission_params)


    def add_permissions_to_user(self, resource_name, resource_id, permissions, to_user_id):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        user_permission_params = {
            "user_id": to_user_id,
            "resource": resource_name,
            "value": resource_id
        }
        for permission in permissions:
            user_permission_params["action"] = permission['action']
            if permission.get('condition'):
                user_permission_params['condition'] = permission['condition']
            self.permission.create(user_permission_params)


    def add_permissions_to_customer(self, resource_name, resource_id, permissions, to_customer_id):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        user_permission_params = {
            "customer_id": to_customer_id,
            "resource": resource_name,
            "value": resource_id
        }
        for permission in permissions:
            user_permission_params["action"] = permission['action']
            if permission.get('condition'):
                user_permission_params['condition'] = permission['condition']
            self.permission.create(user_permission_params)


    def create_permissions_to_group(self, resource_name, resource_id, permissions, to_group_ids):
       #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        # current_user_id = self.token_controller.find_user_id(access_token)
        #
        # # if the current is admin, allow it
        # if self.is_admin(current_user_id):
        #     return self.add_permissions_to_group(resource_name, resource_id, permissions, to_group_id)

        if not self.is_admin:
            customer_id = None
            user_id = None
            if self.is_customer_admin:
                customer_id = self.customer_id
            else:
                user_id = self.user_id
            groups = self.group.find_by_ids(to_group_ids, customer_id= customer_id, user_id=user_id)
            if len(groups) != len(to_group_ids):
                print("len(groups) = {} whereas len(to_group_ids) = {}".format(len(groups), len(to_group_ids)))
                raise Exception("not permitted")

        for to_group_id in to_group_ids:
            self.add_permissions_to_group(resource_name, resource_id, permissions, to_group_id)
        return True

        """
        # if the current user is NOT group admin of the given group, don't allow it
        if not self.is_group_admin(user_id, to_group_id):
            raise Exception("not permitted")
        # if 'create' is NOT in permissions to give
        # and the current user has 'create' permission in the speicified resource, allow it
        # if the specified group has a permission to 'create' on the specified resource, allow it
        if self.PERMISSION_TO_CREATE not in permissions:
            params = {
                'action': 'create',
                'resource': resource_name,
                'value': resource_id
            }
            if self.is_permitted(access_token, params):
                return self.add_permissions_to_group(resource_name, resource_id, permissions, to_group_id)
        """

        #raise Exception("not permitted")


    def create_permissions_to_users(self, resource_name, resource_id, permissions, to_user_ids):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        if not self.is_admin:
            customer_id = None
            user_id = None
            if self.is_customer_admin:
                customer_id = self.customer_id
            else:
                user_id = self.user_id
            users = self.user.find_by_ids(to_user_ids, customer_id= customer_id, user_id=user_id)
            if len(users) != len(to_user_ids):
                print("len(users) = {} whereas len(to_user_ids) = {}".format(len(groups), len(to_user_ids)))
                raise Exception("not permitted")

        # if the current user is admin, allow it
        for to_user_id in to_user_ids:
            self.add_permissions_to_user(resource_name, resource_id, permissions, to_user_id)
        return True

        """
        # if 'create' is NOT in permissions to give
        # and the current user has 'create' permission in the speicified resource, allow it
        # if the specified group has a permission to 'create' on the specified resource, allow it
        if self.PERMISSION_TO_CREATE not in permissions:
            params = {
                'action': 'create',
                'resource': resource_name,
                'value': resource_id
            }
            if self.is_permitted(access_token, params):
                return self.add_permissions_to_group(resource_name, resource_id, permissions, to_group_id)
        """

        #raise Exception("not permitted")


    def create_permissions_to_customer(self, resource_name, resource_id, permissions, to_customer_id):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        if not self.is_admin:
            # check if this user is in the same customer with the customer to give access
            if self.customer_id != to_customer_id:
                raise Exception("not permitted")

        return self.add_permissions_to_customer(resource_name, resource_id, permissions, to_customer_id)


    def create(self, access_token, params):
        #params: {
        #   'owner_id': '',
        #   'resource_name': '',
        #   'resource_id': '',
        #   'permissions':
        #   [
        #       {"action": "r"}
        #       ...
        #   ]
        #   'to_group_ids'|'to_user_ids|to_customer_id': ''
        #}

        owner_id = params.get('owner_id')

        self.find_user_level(access_token)
        if self.user_id != owner_id:
            raise Exception("not permitted")

        if params.get('to_group_ids'):
            return self.create_permissions_to_groups(params['res_name'], params['res_id'], params['permissions'], params.get('to_group_ids'))
        elif params.get('to_user_ids'):
            return self.create_permissions_to_users(params['res_name'], params['res_id'], params['permissions'], params['to_user_ids'])
        elif params.get('to_customer_id'):
            return self.create_permissions_to_customer(params['res_name'], params['res_id'], params['permissions'], params['to_customer_id'])
        raise Exception("not supported")


    def update(self, access_token, params):
        user_id = self.find_user_id(access_token)
        raise Exception("not supported")


    def delete(self, access_token, params):
        user_id = self.find_user_id(access_token)
        return self.permission.delete(params)


    def _filter_conditions(self, user_id, rows):

        filtered = [ row for row in rows if not row.get('condition') ]
        if len(filtered) == len(filtered):
            # there is no row with a condition
            return rows

        permissions = [ row for row in rows if row.get('condition') ]
        for permission in permissions:
            condition = json.loads(permission['condition'])
            # check when the condition is 'is_admin' and it is satisified, add it to the return list if so
            if 'is_admin' in condition:
                if not user_id \
                or not condition['is_admin'] \
                or ( permission.get('group_id') and self.is_group_admin(user_id, permission['group_id']) ):
                    filtered.append(permission)

        return filtered


    def find(self, access_token, params):
        """
        possible attributes in params
            - None
            - [user_id | group_id], action, resource, [value]
        """

        search_params = {}
        if params:
            if 'resource' in params:
                search_params['res_name'] = params['resource']
            if 'action' in params:
                search_params['action'] = params['action']
            if 'value' in params:
                search_params['value'] = params['value']

        self.find_user_level(access_token)

        search_cid = None
        search_gids = None
        search_uids = None
        if not self.is_admin:
            customer_id = None
            user_id = None
            if self.is_customer_admin:
                customer_id = self.customer_id
            else:
                user_id = self.user_id
            groups = self.group.find({}, customer_id= customer_id, user_id=user_id)
            users = self.user.find_({}, customer_id= customer_id, user_id=user_id)

            search_cid = self.customer_id
            search_gids = [g['id'] for g in groups]
            search_uids = [u['id'] for u in users]

        ret = self.permission.find_resource_permissions(search_params, search_cid, search_gids, search_uids)
        if params.get("value_only"):
            ret = self.get_values(ret)

        return ret


    def get_values(self, permissions):
        ret = []
        for permission in permissions:
            if permission['value'] not in ret:
                ret.append(permission['value'])
        return ret
