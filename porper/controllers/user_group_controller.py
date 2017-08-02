
ADMIN_GROUP_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'

class UserGroupController:

    def __init__(self, connection):
        self.connection = connection
        from porper.models.user import User
        from porper.models.group import Group
        from porper.models.user_group import UserGroup
        self.user = User(connection)
        self.group = Group(connection)
        self.user_group = UserGroup(connection)

    def find(self, access_key, params):
        if params.get('user_id'):
            return _find_by_user_id(params['user_id'])
        elif params.get('group_id'):
            return _find_by_group_id(params['group_id'])
        return []

    def _find_by_user_id(self, user_id):
        user_groups = self.user_group.find({'user_id': user_id})
        print user_groups
        ids = [ user_group['group_id'] for user_group in user_groups ]
        if ADMIN_GROUP_ID in ids:
            params = {}
        else:
            #ids = [ user_group['group_id'] for user_group in user_groups if user_group['is_admin'] ]
            ids = [ user_group['group_id'] for user_group in user_groups ]
            params = {'ids': ids}
        print params
        return self.group.find(params)

    def _find_by_group_id(self, group_id):
        user_groups = self.user_group.find({'group_id': group_id})
        print user_groups
        ids = [row['user_id'] for row in user_groups]
        params = {'ids': ids}
        print params
        return self.user.find(params)
