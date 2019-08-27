
from porper.controllers.meta_resource_controller import MetaResourceController

class UserGroupController(MetaResourceController):

    def __init__(self, connection=None):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.user import User
        from porper.models.group import Group
        from porper.models.user_group import UserGroup
        self.user = User(self.connection)
        self.group = Group(self.connection)
        self.user_group = UserGroup(self.connection)
        #from porper.controllers.token_controller import TokenController
        #self.token_controller = TokenController(self.connection)
        #from porper.controllers.permission_controller import PermissionController
        #self.permission_controller = PermissionController(self.connection)


    def create(self, access_token, params):
        """
        possible attributes in params
            - user_id, group_id, is_admin
        """

        if 'is_admin' in params:
            del params['is_admin']

        self.find_user_level(access_token)
        if self.is_admin:
            return self.user_group.create(params)
        elif self.is_customer_admin:
            # check if the user and group belongs to this customer
            ret = self.user.find({'user_id': params['user_id']}, customer_id=self.customer_id)
            if not ret:
                raise Exception('not permitted')
            ret = self.group.find({'group_id': params['group_id']}, customer_id=self.customer_id)
            if not ret:
                raise Exception('not permitted')
            return self.user_group.create(params)
        else:
            raise Exception('not permitted')


    def delete(self, access_token, params):
        """
        possible attributes in params
            - user_id, group_id
        """
        self.find_user_level(access_token)
        if self.is_admin:
            return self.user_group.delete(user_id=params.get('user_id'), group_id=params.get('group_id'))
        elif self.is_customer_admin:
            # check if the user and group belongs to this customer
            ret = self.user.find({'user_id': params['user_id']}, customer_id=self.customer_id)
            if not ret:
                raise Exception('not permitted')
            ret = self.group.find({'group_id': params['group_id']}, customer_id=self.customer_id)
            if not ret:
                raise Exception('not permitted')
            return self.user_group.delete(user_id=params.get('user_id'), group_id=params.get('group_id'))
        else:
            raise Exception('not permitted')


    def find(self, access_token, params):
        """
        possible attributes in params
            - user_id
            - group_id
            - user_ids
            - group_ids
        """
        self.find_user_level(access_token)
        if self.is_admin:
            return self.user_group.find(params)
        if self.is_customer_admin:
            return self.user_group.find(params, customer_id=self.customer_id)
        else:
            return self.user_group.find(params, user_id=self.user_id)


    # def find_by_user_id(self, current_user, user_id):
    #
    #     # find all groups where the given user belongs
    #     user_groups = self.user_group.find({'user_id': user_id})
    #     print(user_groups)
    #     #group_ids = [ user_group['group_id'] for user_group in user_groups ]
    #     #if len(group_ids) == 0: return []
    #
    #     # if this user is admin, return all found groups
    #     if current_user['level'] == self.USER_LEVEL_ADMIN:
    #         #params = {'ids': group_ids}
    #         #print params
    #         #return self.group.find(params)
    #         return user_groups
    #
    #     # return only the groups where the current user belongs
    #     my_user_groups = self.user_group.find({'user_id': current_user['id']})
    #     print(my_user_groups)
    #     if len(my_user_groups) == 0: return []
    #     my_group_ids = [ my_user_group['group_id'] for my_user_group in my_user_groups ]
    #     #allowed_ids = [group_id for group_id in group_ids if group_id in my_group_ids]
    #     #if len(allowed_ids) == 0: return []
    #     #params = {'ids': allowed_ids}
    #     #print params
    #     #return self.group.find(params)
    #     #return allowed_ids
    #     return [user_group for user_group in user_groups if user_group['group_id'] in my_group_ids]
    #
    #
    # def find_by_group_id(self, current_user, group_id):
    #
    #     user_groups = self.user_group.find({'group_id': group_id})
    #     print(user_groups)
    #     user_ids = [ user_group['user_id'] for user_group in user_groups ]
    #     #if len(user_ids) == 0: return []
    #
    #     if current_user['level'] == self.USER_LEVEL_ADMIN or current_user['id'] in user_ids:
    #         #params = {'ids': user_ids}
    #         #print params
    #         #return self.user.find(params)
    #         #return user_ids
    #         return user_groups
    #
    #     return []
    #
    #
    # def find_by_user_ids(self, current_user, user_ids):
    #
    #     user_groups = self.user_group.find_by_user_ids(user_ids)
    #     print(user_groups)
    #     #if len(user_groups) == 0: return []
    #
    #     if current_user['level'] == self.USER_LEVEL_ADMIN:
    #         #user_ids = [ user_group['user_id'] for user_group in user_groups ]
    #         # return unique ids
    #         #return list(set(user_ids))
    #         return user_groups
    #
    #     #allowed_user_groups = [ user_group for user_group in user_groups if user_group['user_id'] == current_user['id']]
    #     #user_ids = [ user_group['user_id'] for user_group in allowed_user_groups ]
    #     #return user_ids
    #     my_user_group_ids = self.user_group.find_by_user_ids([current_user['id']])
    #     my_group_ids = [ my_user_group['group_id'] for my_user_group in my_user_group_ids ]
    #     return [ user_group for user_group in user_groups if user_group['group_id'] in my_group_ids ]
    #
    #
    # def find_by_group_ids(self, current_user, group_ids):
    #
    #     user_groups = self.user_group.find_by_group_ids(group_ids)
    #     print(user_groups)
    #     #if len(user_groups) == 0: return []
    #
    #     if current_user['level'] == self.USER_LEVEL_ADMIN:
    #         #user_ids = [ user_group['user_id'] for user_group in user_groups ]
    #         # return unique ids
    #         #return list(set(user_ids))
    #         return user_groups
    #
    #     #allowed_user_groups = [ user_group for user_group in user_groups if user_group['user_id'] == current_user['id']]
    #     #user_ids = [ user_group['user_id'] for user_group in allowed_user_groups ]
    #     #return user_ids
    #     my_group_ids = [ user_group['group_id'] for user_group in user_groups if user_group['user_id'] == current_user['id'] ]
    #     return [ user_group for user_group in user_groups if user_group['group_id'] in my_group_ids ]
