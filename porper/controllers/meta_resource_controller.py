
import uuid
import json

class MetaResourceController:

    def __init__(self, connection):
        self.connection = connection
        from porper.models.user_group import UserGroup
        self.user_group = UserGroup(connection)
        from porper.models.group import Group
        self.group = Group(connection)
        from porper.controllers.token_controller import TokenController
        self.token_controller = TokenController(self.connection)

        self.USER_LEVEL_ADMIN = 'admin'
        self.USER_LEVEL_GROUP_ADMIN = 'group_admin'
        self.USER_LEVEL_USER = 'user'


    @property
    def model_name(self):
        return self.model.__class__.__name__


    def is_admin(self, user_id):
        user_groups = self.user_group.find({'user_id': user_id})
        group_ids = [ user_group['group_id'] for user_group in user_groups]
        groups = self.group.find_by_ids(group_ids)
        print("groups = {}".format(groups))
        for group in groups:
            if self.group.is_admin_group(group):
                return True
        return False

    def is_group_admin(self, user_id, group_id):
        rows = self.user_group.find({'user_id': user_id, 'group_id': group_id})
        if len(rows) > 0 and rows[0]['is_admin']:  return True
        else: return False

    def is_member(self, user_id, group_id):
        rows = self.user_group.find({'user_id': user_id, 'group_id': group_id})
        if len(rows) > 0:  return True
        else: return False

    def find_user_level(self, access_token, group_id=None):
        user_level = self.USER_LEVEL_USER
        user_id = self.token_controller.find_user_id(access_token)
        if self.is_admin(user_id):
            user_level = self.USER_LEVEL_ADMIN
        elif group_id and self.is_group_admin(user_id, group_id):
            user_level = self.USER_LEVEL_GROUP_ADMIN
        return {"id": user_id, "level": user_level, "group_id": group_id}

    def find_user_val(self, access_token):
        #This is used only for the invite block
        user_id = self.token_controller.find_user_id(access_token)
        return {"id": user_id}
