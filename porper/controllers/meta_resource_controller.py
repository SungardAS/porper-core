
import os
import uuid
import json
import pymysql
import logging
import aws_lambda_logging

from porper.models.permission import PERMISSION_READ, PERMISSION_WRITE
from porper.models.permission import ADMIN_PERMISSION, CUSTOMER_ADMIN_PERMISSION

class MetaResourceController:

    def __init__(self, connection=None):

        if not connection:
            host = os.environ.get('MYSQL_HOST')
            username = os.environ.get('MYSQL_USER')
            password = os.environ.get('MYSQL_PASSWORD')
            database = os.environ.get('MYSQL_DATABASE')
            self.connection = pymysql.connect(host, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor)
            print("@@@@@@@@new connection created")
        else:
            self.connection = connection

        from porper.models.customer import Customer
        self.customer = Customer(self.connection)
        from porper.models.group import Group
        self.group = Group(self.connection)
        from porper.models.access_token import AccessToken
        self.access_token = AccessToken(self.connection)
        from porper.models.permission import Permission
        self.permission = Permission(self.connection)
        # from porper.models.user_group import UserGroup
        # self.user_group = UserGroup(self.connection)
        # from porper.controllers.token_controller import TokenController
        # self.token_controller = TokenController(self.connection)

        self.permissions = None
        self.user_id = None
        self.customer_id = None
        self.permission_name = None
        self.is_admin = False
        self.is_customer_admin = False

        self.permission_read = PERMISSION_READ
        self.permission_write = PERMISSION_WRITE

        # self.USER_LEVEL_ADMIN = 'admin'
        # self.USER_LEVEL_CUSTOMER_ADMIN = 'customer_admin'
        # # self.USER_LEVEL_GROUP_ADMIN = 'group_admin'
        # self.USER_LEVEL_USER = 'user'

        self.logger = logging.getLogger()
        loglevel = "INFO"
        logging.basicConfig(level=logging.ERROR)
        aws_lambda_logging.setup(level=loglevel)


    @property
    def model_name(self):
        return self.model.__class__.__name__


    # def find_permissions(self, user_id):
    #     sql = """
    #         select p.res_name name, p.action action, p.value value
    #         from User u
    #         inner join Group_User gu on gu.user_id = u.id
    #         inner join `Group` g on g.id = gu.group_id
    #         inner join Role r on g.role_id = r.id
    #         inner join Role_Function rf on rf.role_id = r.id
    #         inner join Function f on rf.function_id = f.id
    #         inner join Function_Permission fp on fp.function_id = f.id
    #         inner join Permission p on fp.permission_id = p.id
    #         where p.group_id is null and p.user_id is null and u.id = '{}'
    #     """
    #     return self.find_by_sql(sql.format(user_id))


    # def find_permissions(self, user_id, name, action, value=None):
    #
    #     sql = """
    #         select f.id function_id, f.name function_name, p.id permission_id,
    #         p.res_name resource_name, p.action action, p.value resource_id
    #         from User u
    #         inner join Group_User gu on gu.user_id = u.id
    #         inner join `Group` g on g.id = gu.group_id
    #         inner join Role r on g.role_id = r.id
    #         inner join Role_Function rf on rf.role_id = r.id
    #         inner join Function f on rf.function_id = f.id
    #         inner join Function_Permission fp on fp.function_id = f.id
    #         inner join Permission p on fp.permission_id = p.id
    #         where u.id = '{}' and p.res_name = '{}' and p.action = '{}'
    #     """
    #     if value:
    #         sql += " and p.value = '{}'".format(value)
    #
    #     return self.find_by_sql(sql.format(user_id))
    #     # if rows:
    #     #     return (True, rows[0]['resource_id'])
    #     # return (False, None)


    def find_current_user(self, access_token):
        return self.access_token.find_user(access_token)


    # def is_admin(self, user_id):
    #     rows = self.find_permissions(user_id, ADMIN_PERMISSION, PERMISSION_WRITE)
    #     if rows:
    #         return True
    #     return False
    #
    #
    # def is_customer_admin(self, user_id, customer_id=None, group_id=None):
    #
    #     if customer_id is None and group_id:
    #         # find the customer_id of this given group
    #         row = self.group.find_by_id(group_id)
    #         if row:
    #             customer_id = row['customer_id']
    #
    #     rows = self.find_permissions(user_id, CUSTOMER_ADMIN_PERMISSION, PERMISSION_WRITE, customer_id)
    #     if rows:
    #         return rows[0]['customer_id']
    #     return None
    #
    #
    # # def is_group_admin(self, user_id, group_id):
    # #     rows = self.user_group.find({'user_id': user_id, 'group_id': group_id})
    # #     if len(rows) > 0 and rows[0]['is_admin']:  return True
    # #     else: return False


    def find_user_level(self, access_token):
        self.user_id = self.find_current_user(access_token)['id']
        self.permissions = self.permission.find({'user_id': self.user_id})
        self.customer_id = self.customer.find({'user_id': self.user_id})[0]['id']

        if [p for p in self.permissions if p['name'] == ADMIN_PERMISSION]:
            self.is_admin = True
        elif [p for p in self.permissions if p['name'] == CUSTOMER_ADMIN_PERMISSION]:
            self.is_customer_admin = True

        # def is_admin(self):
        #     return self.level == USER_LEVEL_ADMIN
        #
        #
        # def is_customer_admin(self):
        #     return self.level == USER_LEVEL_CUSTOMER_ADMIN
        #
        #
        # def is_user(self):
        #     return self.level == USER_LEVEL_USER



    # def find_user_val(self, access_token):
    #     #This is used only for the invite block
    #     user_id = self.token_controller.find_user_id(access_token)
    #     return {"id": user_id}


    def is_permitted(self, name, action, value=None):
        # if self.is_admin():
        #     return True
        # if self.is_customer_admin():
        #     if name in ADMIN_PERMISSIONS and action == PERMISSION_WRITE:
        #         return False
        #     else:
        #         return True
        permitted = [p['value'] for p in self.permissions if p['name'] == name and p['action'] == action]
        if not permitted:
            return False
        if value and value not in permitted:
            return False
        return True


    def is_member(self, customer_id=None, group_id=None):
        if self.is_admin:
            return True
        if customer_id:
            return self.customer_id == customer_id
        else:
            if self.is_customer_admin:
                if self.group.find({'group_id': group_id}, self.customer_id):
                    return True
            else:
                if self.group.find({'group_id': group_id}, self.user_id):
                    return True
        return False


    def commit(self):
        self.connection.commit()


    def rollback(self):
        self.connection.rollback()
