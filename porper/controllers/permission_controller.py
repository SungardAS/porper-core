
import json
from porper.controllers.meta_resource_controller import MetaResourceController

class PermissionController(MetaResourceController):

    def __init__(self, connection=None, loglevel="INFO"):
        MetaResourceController.__init__(self, connection, loglevel)
        from porper.models.permission import Permission
        from porper.models.user_group import UserGroup
        self.permission = Permission(self.connection, loglevel)
        self.user_group = UserGroup(self.connection, loglevel)
        from porper.models.user import User
        from porper.models.group import Group
        self.user = User(self.connection, loglevel)
        self.group = Group(self.connection, loglevel)
        from porper.models.access_token import AccessToken
        self.access_token = AccessToken(self.connection, loglevel)
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


    def add_permissions_to_groups(self, resource_name, resource_id, permissions):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        permission_params = {
            "resource": resource_name,
            "value": resource_id
        }
        for permission in permissions:
            permission_params["group_id"] = permission['id']
            permission_params["action"] = permission['action']
            if permission.get('condition'):
                permission_params['condition'] = permission['condition']
            if permission['state'].lower() == "a":
                self.permission.create(permission_params)
            elif permission['state'].lower() == "u":
                self.permission.update(permission_params)
            elif permission['state'].lower() == "d":
                self.permission.delete(permission_params)


    def add_permissions_to_users(self, resource_name, resource_id, permissions):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        permission_params = {
            "resource": resource_name,
            "value": resource_id
        }
        for permission in permissions:
            permission_params["user_id"] = permission['id']
            permission_params["action"] = permission['action']
            if permission.get('condition'):
                permission_params['condition'] = permission['condition']
            if permission['state'].lower() == "a":
                self.permission.create(permission_params)
            elif permission['state'].lower() == "u":
                self.permission.update(permission_params)
            elif permission['state'].lower() == "d":
                self.permission.delete(permission_params)


    def add_permissions_to_customers(self, resource_name, resource_id, permissions):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        permission_params = {
            "resource": resource_name,
            "value": resource_id
        }
        for permission in permissions:
            permission_params["customer_id"] = permission['id']
            permission_params["action"] = permission['action']
            if permission.get('condition'):
                permission_params['condition'] = permission['condition']
            if permission['state'].lower() == "a":
                self.permission.create(permission_params)
            elif permission['state'].lower() == "u":
                self.permission.update(permission_params)
            elif permission['state'].lower() == "d":
                self.permission.delete(permission_params)


    def create_permissions_to_groups(self, resource_name, resource_id, to_group_ids):
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
            group_ids = [g['id'] for g in to_group_ids]
            customer_id = None
            user_id = None
            # if self.is_customer_admin:
            #     customer_id = self.customer_id
            # else:
            #     user_id = self.user_id
            # allow all users in the same customer
            customer_id = self.customer_id
            groups = self.group.find_by_ids(group_ids, customer_id= customer_id, user_id=user_id)
            if len(groups) != len(group_ids):
                self.logger.info("len(groups) = {} whereas len(to_group_ids) = {}".format(len(groups), len(group_ids)))
                raise Exception("not permitted")

        return self.add_permissions_to_groups(resource_name, resource_id, to_group_ids)

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


    def create_permissions_to_users(self, resource_name, resource_id, to_user_ids):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        if not self.is_admin:
            user_ids = [u['id'] for u in to_user_ids]
            customer_id = None
            user_id = None
            # if self.is_customer_admin:
            #     customer_id = self.customer_id
            # else:
            #     user_id = self.user_id
            # allow all users in the same customer
            customer_id = self.customer_id
            users = self.user.find_by_ids(user_ids, customer_id=customer_id, user_id=user_id)
            if len(users) != len(user_ids):
                self.logger.info("len(users) = {} whereas len(to_user_ids) = {}".format(len(users), len(user_ids)))
                raise Exception("not permitted")

        return self.add_permissions_to_users(resource_name, resource_id, to_user_ids)

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


    def create_permissions_to_customer(self, resource_name, resource_id, to_customer_ids):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        if not self.is_admin:
            # check if this user is in the same customer with the customer to give access
            for customer_id in [c['id'] for c in to_customer_ids]:
                if self.customer_id != to_customer_id:
                    raise Exception("not permitted")

        return self.add_permissions_to_customers(resource_name, resource_id, to_customer_ids)


    def create(self, access_token, params):
        # {
        #     "owner_id": "35925", "res_name": "meta", "res_id": "d392909c-d15f-43ff-98b4-9fd7e3ca80e9",
        #     "to_user_ids": [{"id": "user1@ctotest.com", "action": "w", "state": "A"},
        #                     {"id": "user2@ctotest.com", "action": "r", "state, "state": "A"}],
        #     "to_group_ids": [{"id": "group_id1", "action": "w", "state": "A"},
        #                     {"id": "group_id2", "action": "r", "state": "A"}],
        #     "to_customer_ids": [{"id": "customer_id1", "action": "w", "state": "A"}
        #                     {"id": "customer_id1", "action": "r", "state": "A"}]
        # }

        owner_id = params.get('owner_id')

        self.find_user_level(access_token)
        if self.user_id != owner_id:
            raise Exception("not permitted")

        if params.get('to_group_ids'):
            self.create_permissions_to_groups(params['res_name'], params['res_id'], params['to_group_ids'])
        if params.get('to_user_ids'):
            self.create_permissions_to_users(params['res_name'], params['res_id'], params['to_user_ids'])
        if params.get('to_customer_ids'):
            self.create_permissions_to_customer(params['res_name'], params['res_id'], params['to_customer_ids'])

        return True


    def update(self, access_token, params):
        user_id = self.find_user_id(access_token)
        raise Exception("not supported")


    # This is to remove all permissions of given resource
    def delete(self, access_token, params):
        user_id = self.find_user_id(access_token)

        owner_id = params.get('owner_id')

        self.find_user_level(access_token)
        if self.user_id != owner_id:
            raise Exception("not permitted")

        if 'res_name' not in params or 'res_id' not in params:
            raise Exception("resource name and id are not provided")

        params['value'] = params['res_id']
        del params['res_id']
        return self.permission.delete(params)


    # def _filter_conditions(self, user_id, rows):
    #
    #     filtered = [ row for row in rows if not row.get('condition') ]
    #     if len(filtered) == len(filtered):
    #         # there is no row with a condition
    #         return rows
    #
    #     permissions = [ row for row in rows if row.get('condition') ]
    #     for permission in permissions:
    #         condition = json.loads(permission['condition'])
    #         # check when the condition is 'is_admin' and it is satisified, add it to the return list if so
    #         if 'is_admin' in condition:
    #             if not user_id \
    #             or not condition['is_admin'] \
    #             or ( permission.get('group_id') and self.is_group_admin(user_id, permission['group_id']) ):
    #                 filtered.append(permission)
    #
    #     return filtered


    def find(self, access_token, params):
        """
        possible attributes in params
            - None
            - [user_id | group_id], action, resource, [value]
        """

        search_params = {}
        if params:
            if 'res_name' in params:
                search_params['res_name'] = params['res_name']
            if 'action' in params:
                search_params['action'] = params['action']
            if 'res_id' in params:
                search_params['value'] = params['res_id']

        self.find_user_level(access_token)
        owner_id = params.get('owner_id')

        search_cid = None
        search_gids = None
        search_uids = None
        if not self.is_admin and owner_id != self.user_id:
            customer_id = None
            user_id = None
            if self.is_customer_admin:
                customer_id = self.customer_id
            else:
                user_id = self.user_id
            groups = self.group.find({}, customer_id= customer_id, user_id=user_id)
            users = self.user.find({}, customer_id= customer_id, user_id=user_id)

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
