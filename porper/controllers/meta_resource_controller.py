
import uuid
import json

ADMIN_GROUP_ID = 'e51a447d-cb0a-4166-870a-d74ce38add35'
PUBLIC_GROUP_ID = '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a'

class MetaResourceController:

    def __init__(self, connection):
        self.connection = connection
        from porper.models.user_group import UserGroup
        self.user_group = UserGroup(connection)
        from porper.controllers.token_controller import TokenController
        #from porper.controllers.permission_controller import PermissionController
        self.token_controller = TokenController(self.connection)
        #self.permission_controller = PermissionController(self.connection)

        self.ADMIN_GROUP_ID = ADMIN_GROUP_ID
        self.USER_LEVEL_ADMIN = 'admin'
        self.USER_LEVEL_GROUP_ADMIN = 'group_admin'
        self.USER_LEVEL_USER = 'user'


    @property
    def model_name(self):
        return self.model.__class__.__name__


    def is_admin(self, user_id):
        row = self.user_group.find({'user_id': user_id, 'group_id': self.ADMIN_GROUP_ID})
        if len(row) > 0:  return True
        else: return False

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


    #def is_group_admin(self, user_id, group_id):
    #    return self.permission_controller.is_group_admin(user_id, group_id)
