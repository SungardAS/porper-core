
ADMIN_GROUP_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'

class GroupController:

    def __init__(self, connection):
        self.connection = connection
        from porper.models.group import Group
        from porper.models.user_group import UserGroup
        self.group = Group(connection)
        self.user_group = UserGroup(connection)
        from porper.controllers.token_controller import TokenController
        self.token_controller = TokenController(connection)
        from porper.controllers.user_group_controller import UserGroupController
        self.user_group_controller = UserGroupController(connection)

    def is_admin(self, user_id):
        row = self.user_group.find({'user_id': user_id, 'group_id': ADMIN_GROUP_ID})
        if len(row) > 0:  return True
        else: return False

    # only the admin can create a group
    def create(self, access_token, params):
        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']
        if not self.is_admin(user_id):  raise Exception("not permitted")
        return self.group.create(params)

    def update(self, access_token, params):
        raise Exception("not supported")

    def delete(self, access_token, params):
        raise Exception("not supported")

    """
    1. find all groups if I'm the admin
    2. find only groups where I'm the group admin
    """
    def find(self, access_token, params=None):
        rows = self.token_controller.find(access_token)
        user_id = rows[0]['user_id']
        return self.user_group_controller.find(access_token, {'user_id': user_id})
