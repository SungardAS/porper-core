
from porper.controllers.meta_resource_controller import MetaResourceController
# import aws_lambda_logging
# import logging

# logger = logging.getLogger()
# loglevel = "INFO"
# logging.basicConfig(level=logging.ERROR)
# aws_lambda_logging.setup(level=loglevel)

class GroupController(MetaResourceController):

    def __init__(self, connection=None):
        #self.connection = connection
        MetaResourceController.__init__(self, connection)
        from porper.models.group import Group
        self.group = Group(self.connection)
        from porper.models.user import User
        self.user = User(self.connection)
        # from porper.controllers.user_group_controller import UserGroupController
        # self.user_group_controller = UserGroupController(self.connection)

        self.permission_name = 'group'


    # only the admin can create a group
    def create(self, access_token, params):
        """
        possible attributes in params
            - [id], name
        """
        self.logger.info(f"params={params}")
        self.logger.info(f"access_token={access_token}")
        # self.logger.info(f"paths={paths}")

        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        if "customer_id" not in params or not self.is_member(customer_id=params['customer_id']):
            raise Exception("not permitted")

        return self.group.create(params)


    def update(self, access_token, params):
        """
        possible attributes in params
            - id, name
        """
        self.logger.info(f'group_controller_update-params={params}')
        self.logger.info(f'group_controller_update-access_token={access_token}')

        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        item = self.group.find_by_id(params['id'])
        if not item or not self.is_member(customer_id=item['customer_id']):
            raise Exception("not permitted")

        if params.get('customer_id'):
            raise Exception('You cannot update the group customer')

        if 'name' in params:
            ret = self.group.find({'name': params['name']})
            if ret and ret[0]['id'] != params['id']:
                raise Exception("the group name already exists")

        return self.group.update(params)


    def delete(self, access_token, params):
        """
        possible attributes in params
            - id
        """

        self.find_user_level(access_token)
        if not self.is_permitted(self.permission_name, self.permission_write):
            raise Exception("not permitted")

        item = self.group.find_by_id(params['id'])
        if not item or not self.is_member(customer_id=item['customer_id']):
            raise Exception("not permitted")

        # cannot remove it when it has users
        users = self.user.find({'group_id': params['id']})
        if len(users) > 0:
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

        self.find_user_level(access_token)
        customer_id = None
        user_id = None
        if self.is_customer_admin:
            customer_id = self.customer_id
        elif not self.is_admin:
            user_id = self.user_id

        if 'ids' in params:
            groups = self.group.find_by_ids(params['ids'], customer_id=customer_id, user_id=user_id)
            return groups

        else:
            groups = self.group.find(params, customer_id=customer_id, user_id=user_id)
            if groups and 'id' in params:
                return groups[0]
            return groups
