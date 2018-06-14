
import uuid
import json

class MetaResourceController:

    def __init__(self, connection):
        self.connection = connection
        from porper.controllers.token_controller import TokenController
        from porper.controllers.permission_controller import PermissionController
        self.token_controller = TokenController(self.connection)
        self.permission_controller = PermissionController(self.connection)

        self.ADMIN_GROUP_ID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
        self.USER_LEVEL_ADMIN = 'admin'
        self.USER_LEVEL_GROUP_ADMIN = 'group_admin'
        self.USER_LEVEL_USER = 'user'


    @property
    def model_name(self):
        return self.model.__class__.__name__


    def find_user_level(self, access_token, group_id=None):
        user_level = self.USER_LEVEL_USER
        user_id = self.token_controller.find_user_id(access_token)
        if self.permission_controller.is_admin(user_id):
            user_level = self.USER_LEVEL_ADMIN
        elif group_id and self.permission_controller.is_group_admin(user_id, group_id):
            user_level = self.USER_LEVEL_GROUP_ADMIN
        return {"id": user_id, "level": user_level, "group_id": group_id}


    def is_group_admin(self, user_id, group_id):
        return self.permission_controller.is_group_admin(user_id, group_id)
