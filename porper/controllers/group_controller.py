
from meta_resource_controller import MetaResourceController

class GroupController(MetaResourceController):

    def __init__(self, connection):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.group import Group
        self.group = Group(connection)
        #from porper.models.user_group import UserGroup
        #self.user_group = UserGroup(connection)
        #from porper.controllers.token_controller import TokenController
        #self.token_controller = TokenController(connection)
        #from porper.controllers.permission_controller import PermissionController
        #self.permission_controller = PermissionController(self.connection)
        from porper.controllers.user_group_controller import UserGroupController
        self.user_group_controller = UserGroupController(self.connection)


    # only the admin can create a group
    def create(self, access_token, params):
        """
        possible attributes in params
            - [id], name
        """
        current_user = self.find_user_level(access_token)
        if current_user['level'] == self.USER_LEVEL_ADMIN:
            return self.group.create(params)
        else:
            raise Exception('not permitted')


    def update(self, access_token, params):
        """
        possible attributes in params
            - id, name
        """
        # now allowed to change the admin group's name
        if params['id'] == self.ADMIN_GROUP_ID:
            raise Exception('You cannot update the admin group')
        current_user = self.find_user_level(access_token, params['id'])
        if current_user['level'] == self.USER_LEVEL_USER:
            raise Exception('not permitted')
        else:
            return self.group.update({'id': params['id'], 'name': params['name']})


    def delete(self, access_token, params):
        """
        possible attributes in params
            - id
        """
        current_user = self.find_user_level(access_token, params['id'])
        if current_user['level'] == self.USER_LEVEL_USER:
            raise Exception('not permitted')

        # cannot remove the admin group
        if params['id'] == self.ADMIN_GROUP_ID:
            raise Exception("You cannot remove the admin group")

        # cannot remove it when it has users
        user_groups = self.user_group_controller.find(access_token, {'group_id': params['id']})
        if len(user_groups) > 0:
            raise Exception("You must remove all users before removing this group")
        return self.group.delete(params['id'])


    def find(self, access_token, params):
        """
        possible attributes in params
            - user_id: find all groups where this given user belongs
            - id: find a specific group
            - ids: find specific groups
            - None: No condition
            - name
        """
        if 'user_id' in params:
            user_groups = self.user_group_controller.find(access_token, {'user_id': params['user_id']})
            group_ids = [ user_group['group_id'] for user_group in user_groups ]
            if len(group_ids) == 0: return []
            return self.group.find_by_ids(group_ids)

        if 'id' in params:
            user_groups = self.user_group_controller.find(access_token, {'group_id': params['id']})
            group_ids = [ user_group['group_id'] for user_group in user_groups ]
            if params['id'] in group_ids:
                return self.group.find_by_id(params['id'])
            else:
                raise Exception('not permitted')

        if 'ids' in params:
            user_groups = self.user_group_controller.find(access_token, {'group_ids': params['ids']})
            group_ids = [ user_group['group_id'] for user_group in user_groups if user_group['group_id'] in params['ids'] ]
            if len(group_ids) == 0: return []
            return self.group.find_by_ids(group_ids)

        # find current user information including id and level
        current_user = self.find_user_level(access_token, params.get('group_id'))

        if not params:
            # in case there is no params
            groups = self.group.find({})
        else:
            # for other parameters
            groups = self.group.find(params)
        if current_user['level'] == self.USER_LEVEL_ADMIN:
            return groups
        # return only the groups where the current user belongs
        user_groups = self.user_group_controller.find(access_token, {'user_id': current_user['id']})
        group_ids = [ user_group['group_id'] for user_group in user_groups]
        return [ group for group in groups if group['id'] in group_ids]
