
from porper.controllers.meta_resource_controller import MetaResourceController
import aws_lambda_logging
import logging

logger = logging.getLogger()
loglevel = "INFO"
logging.basicConfig(level=logging.ERROR)
aws_lambda_logging.setup(level=loglevel)

class GroupController(MetaResourceController):

    def __init__(self, connection):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.group import Group
        self.group = Group(connection)
        from porper.controllers.user_group_controller import UserGroupController
        self.user_group_controller = UserGroupController(self.connection)


    # only the admin can create a group
    def create(self, access_token, params, paths=None):
        """
        possible attributes in params
            - [id], name
        """
        logger.info(f"params={params}")
        logger.info(f"access_token={access_token}")
        logger.info(f"paths={paths}")
        current_user = self.find_user_level(access_token)
        if current_user['level'] != self.USER_LEVEL_ADMIN:
            raise Exception('not permitted')

        # check if the group with the given customer already exists
        ret = self.group.find({"name": params["name"], "customer_id": params["customer_id"]})
        if ret:
            raise Exception("already exists")

        return self.group.create(params, paths)


    def update(self, access_token, params, paths=None):
        """
        possible attributes in params
            - id, name
        """
        logger.info(f'group_controller_update-params={params}')
        logger.info(f'group_controller_update-access_token={access_token}')
        if params.get('customer_id'):
            raise Exception('You cannot update the group customer')
        current_user = self.find_user_level(access_token, params['id'])
        if current_user['level'] == self.USER_LEVEL_USER:
            raise Exception('not permitted')
        else:
            return self.group.update(params)


    def delete(self, access_token, params, paths=None):
        """
        possible attributes in params
            - id
        """
        current_user = self.find_user_level(access_token, params['id'])
        if current_user['level'] == self.USER_LEVEL_USER:
            raise Exception('not permitted')

        # cannot remove it when it has users
        user_groups = self.user_group_controller.find(access_token, {'group_id': params['id']})
        if len(user_groups) > 0:
            raise Exception("You must remove all users before removing this group")
        return self.group.delete(params['id'])


    def find(self, access_token, params, paths=None):
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
            if len(user_groups) == 0:
               return self.group.find_by_id(params['id'])
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
