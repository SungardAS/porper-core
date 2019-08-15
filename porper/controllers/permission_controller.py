
import json

class PermissionController:

    def __init__(self, connection):
        self.connection = connection
        from porper.models.permission import Permission
        from porper.models.user_group import UserGroup
        self.permission = Permission(connection)
        self.user_group = UserGroup(connection)
        from porper.models.group import Group
        self.group = Group(connection)
        from porper.controllers.token_controller import TokenController
        self.token_controller = TokenController(connection)
        from porper.controllers.user_group_controller import UserGroupController
        self.user_group_controller = UserGroupController(connection)

        from porper.models.permission import ALL
        self.PERMITTED_TO_ALL = ALL


    def is_admin(self, user_id):
        return self.user_group_controller.is_admin(user_id)

    def is_group_admin(self, user_id, group_id):
        return self.user_group_controller.is_group_admin(user_id, group_id)

    def is_member(self, user_id, group_id):
        return self.user_group_controller.is_member(user_id, group_id)

    def is_permitted(self, access_token, params):
        """
        possible attributes in params
            - None
            - [user_id | group_id], action, resource, value
        """
        current_user_id = self.token_controller.find_user_id(access_token)
        if self.is_admin(current_user_id):    return True

        #params['all'] = True
        rows = self.find(access_token, params)
        print("permitted : {}".format(rows))
        if len(rows) == 0:  return False
        return True


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


    def create_permissions_to_groups(self, current_user_id, resource_name, resource_id, permissions, to_group_ids):
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

        if not self.is_admin(current_user_id):

            # check if this user is in the same customer with the groups to give access
            user_groups = self.user_group.find({'user_id': current_user_id})
            current_user_customer_id = self.group.find_by_id(user_groups[0]['group_id'])['customer_id']

            to_groups = self.group.find_by_ids(to_group_ids)
            for to_group in to_groups:
                print("current_user_customer_id = {}".format(current_user_customer_id))
                print("group {}, customer_id = {}".format(to_group['id'], to_group['customer_id']))
                if to_group['customer_id'] != current_user_customer_id:
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


    def create_permissions_to_users(self, current_user_id, resource_name, resource_id, permissions, to_user_ids):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        if not self.is_admin(current_user_id):

            # check if this user is in the same customer with the users to give access
            user_groups = self.user_group.find({'user_id': current_user_id})
            current_user_customer_id = self.group.find_by_id(user_groups[0]['group_id'])['customer_id']

            user_groups = self.user_group.find_by_user_ids(to_user_ids)
            to_groups = self.group.find_by_ids([ug['group_id'] for ug in user_groups])
            for to_group in to_groups:
                if to_group['customer_id'] != current_user_customer_id:
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


    def create_permissions_to_customer(self, current_user_id, resource_name, resource_id, permissions, to_customer_id):
        #permissions:
        #[
        #    {"action": "r"},
        #    ...
        #]

        if not self.is_admin(current_user_id):
            # check if this user is in the same customer with the customer to give access
            user_groups = self.user_group.find({'user_id': current_user_id})
            current_user_customer_id = self.group.find_by_id(user_groups[0]['group_id'])['customer_id']
            if current_user_customer_id != to_customer_id:
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

        owner_id = params['owner_id']
        current_user_id = self.token_controller.find_user_id(access_token)
        if current_user_id != owner_id:
            raise Exception("not permitted")

        if params.get('to_group_ids') or params.get('to_group_ids'):
            return self.create_permissions_to_groups(current_user_id, params['res_name'], params['res_id'], params['permissions'], params.get('to_group_ids'))
        elif params.get('to_user_ids'):
            return self.create_permissions_to_users(current_user_id, params['res_name'], params['res_id'], params['permissions'], params['to_user_ids'])
        elif params.get('to_customer_id'):
            return self.create_permissions_to_customer(current_user_id, params['res_name'], params['res_id'], params['permissions'], params['to_customer_id'])
        raise Exception("not supported")


    def update(self, access_token, params):
        user_id = self.token_controller.find_user_id(access_token)
        raise Exception("not supported")


    def delete(self, access_token, params):
        user_id = self.token_controller.find_user_id(access_token)
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

        group_search_params = {}
        user_search_params = {}
        customer_search_params = {}
        current_user_id = self.token_controller.find_user_id(access_token)

        if not self.is_admin(current_user_id):
            user_groups = self.user_group.find({'user_id': current_user_id})
            current_user_customer_id = self.group.find_by_id(user_groups[0]['group_id'])['customer_id']
            current_user_group_ids = [ug['group_id'] for ug in user_groups]
            group_search_params = {
                'group_ids': current_user_group_ids
            }
            user_search_params = {
                'user_id': current_user_id
            }
            customer_search_params = {
                'customer_id': current_user_customer_id
            }

        if params:
            if params.get("res_id"):
                group_search_params['value'] = params['res_id']
                user_search_params['value'] = params['res_id']
                customer_search_params['value'] = params['res_id']
            if params.get("res_name"):
                group_search_params['resource'] = params['res_name']
                user_search_params['resource'] = params['res_name']
                customer_search_params['resource'] = params['res_name']
            if params.get("action"):
                group_search_params['action'] = params['action']
                user_search_params['action'] = params['action']
                customer_search_params['action'] = params['action']

        print("group_search_params = {}".format(group_search_params))
        print("user_search_params = {}".format(user_search_params))
        print("customer_search_params = {}".format(customer_search_params))

        ret = self.permission.find(group_search_params)

        if not self.is_admin(current_user_id):
            ret += self.permission.find(user_search_params)
            ret += self.permission.find(customer_search_params)

        # if params.get('group_id'):
        #
        #     rows = self.permission.find({
        #         'action': params.get('action'),
        #         'resource': params.get('resource'),
        #         'value': params.get('value')
        #     })
        # if len(rows) == 0:  return []
        #
        # current_user_id = self.token_controller.find_user_id(access_token)
        #
        # if not params or (not params.get('group_id') and not params.get('user_id')):
        #
        #     if self.is_admin(current_user_id):
        #         if params.get("value_only"):
        #             #rows = self.get_values(rows)
        #             rows = [self.PERMITTED_TO_ALL]
        #         return rows
        #
        #     # find all 'group_ids' where the current user
        #     user_id = current_user_id
        #     user_groups = self.user_group_controller.find(access_token, {'user_id': user_id})
        #     group_ids = [ user_group['group_id'] for user_group in user_groups]
        #
        # elif params.get('group_id'):
        #
        #     user_id = None
        #
        #     # find all 'group_ids' where the current user belongs
        #     if self.is_admin(current_user_id):
        #         group_ids = [ params['group_id'] ]
        #     else:
        #         current_user_user_groups = self.user_group_controller.find(access_token, {'user_id': current_user_id} )
        #         current_user_group_ids = [ user_group['group_id'] for user_group in current_user_user_groups ]
        #         if params['group_id'] in current_user_group_ids:
        #             group_ids = [ params['group_id'] ]
        #         else:
        #             group_ids = []
        #
        # elif params.get('user_id'):
        #
        #     user_id = params['user_id']
        #
        #     # find all 'group_ids' where the given user belongs
        #     given_user_user_groups = self.user_group_controller.find(access_token, {'user_id': user_id})
        #     given_user_group_ids = [ user_group['group_id'] for user_group in given_user_user_groups ]
        #
        #     if self.is_admin(current_user_id):
        #         group_ids = given_user_group_ids
        #     else:
        #         # find all 'group_ids' where the current user belongs
        #         current_user_user_groups = self.user_group_controller.find(access_token, {'user_id': current_user_id})
        #         current_user_group_ids = [ user_group['group_id'] for user_group in current_user_user_groups ]
        #
        #         # allow only the groups where the current user belongs
        #         group_ids = [ group_id for group_id in given_user_group_ids if group_id in current_user_group_ids ]
        #
        # else:
        #     raise Exception("not supported params: {}".format(params))
        #
        # # if there is no common group, return empty to prevent from returning permissions to '*'
        # if not self.is_admin(current_user_id) and len(group_ids) == 0:
        #     return []
        #
        # # choose only the allowd by user_id & its groups
        # if user_id is None:
        #     rows = [ row for row in rows if row.get('group_id') and (row['group_id'] in group_ids or row['group_id'] == self.PERMITTED_TO_ALL) ]
        # else:
        #     rows = [ row for row in rows if (row.get('user_id') and (row['user_id'] == user_id or row['user_id'] == self.PERMITTED_TO_ALL)) or (row.get('group_id') and (row['group_id'] in group_ids or row['group_id'] == self.PERMITTED_TO_ALL)) ]

        if len(ret) == 0:  return []

        # ret = self._filter_conditions(user_id, rows)

        print(params.get("value_only"))
        if params.get("value_only"):
            ret = self.get_values(ret)

        return ret

    def get_values(self, permissions):
        ret = []
        for permission in permissions:
            if permission['value'] not in ret:
                ret.append(permission['value'])
        return ret
