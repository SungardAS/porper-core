
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource
from porper.models.permission import ADMIN_PERMISSION, CUSTOMER_ADMIN_PERMISSION

class Group(Resource):

    def __init__(self, connection=None):
        Resource.__init__(self, connection)
        self.table_name = "`Group`"


    def find_admin_groups(self, user_id=None):

        sql = """
            select distinct g.*
            from `Group` g
        """
        if user_id:
            sql += " inner join Group_User gu on g.id = gu.group_id"

        sql += """
            inner join Role r on g.role_id = r.id
            inner join Role_Function rf on rf.role_id = r.id
            inner join Function f on rf.function_id = f.id
            inner join Function_Permission fp on fp.function_id = f.id
            inner join Permission p on fp.permission_id = p.id
            where p.res_name = '{}'
        """
        if user_id:
            sql += " and gu.user_id = '{}'".format(user_id)

        return self.find_by_sql(sql.format(ADMIN_PERMISSION))


    def find_custom_admin_groups(self, user_id=None, customer_id=None, group_id=None):

        sql = """
            select distinct g.*
            from `Group` g
            inner join Group_User gu on g.id = gu.group_id
            inner join Role r on g.role_id = r.id
            inner join Role_Function rf on rf.role_id = r.id
            inner join Function f on rf.function_id = f.id
            inner join Function_Permission fp on fp.function_id = f.id
            inner join Permission p on fp.permission_id = p.id
            where p.res_name = '{}'
        """
        if customer_id:
            sql += " and g.customer_id = '{}'".format(customer_id)
        if group_id:
            sql += " and gu.group_id = '{}'".format(group_id)
        if user_id:
            sql += " and gu.user_id = '{}'".format(user_id)

        return self.find_by_sql(sql.format(CUSTOMER_ADMIN_PERMISSION))


    # def is_admin_group(self, group_id):
    #
    #     res_name = ADMIN_PERMISSION['resource']
    #     action = ADMIN_PERMISSION['action']
    #
    #     sql = """
    #         select distinct p.res_name resource, p.action action
    #         from `Group` g
    #         inner join Role r on g.role_id = r.id
    #         inner join Role_Function rf on rf.role_id = r.id
    #         inner join Function f on rf.function_id = f.id
    #         inner join Function_Permission fp on fp.function_id = f.id
    #         inner join Permission p on fp.permission_id = p.id
    #         where g.id = '{}'
    #         and p.res_name = '{}' and p.action = '{}'
    #     """
    #
    #     row = self.find_one(sql.format(group_id, res_name, action))
    #     if row:
    #         return True
    #
    #     return False
    #
    #
    # def is_custom_admin_group(self, group_id, customer_id):
    #
    #     res_name = CUSTOMER_ADMIN_PERMISSION['resource']
    #     action = CUSTOMER_ADMIN_PERMISSION['action']
    #
    #     sql = """
    #         select distinct p.res_name resource, p.action action
    #         from `Group` g
    #         inner join Role r on g.role_id = r.id
    #         inner join Role_Function rf on rf.role_id = r.id
    #         inner join Function f on rf.function_id = f.id
    #         inner join Function_Permission fp on fp.function_id = f.id
    #         inner join Permission p on fp.permission_id = p.id
    #         where g.id = '{}'
    #         and p.res_name = '{}' and p.action = '{}' and p.value = '{}'
    #     """
    #
    #     row = self.find_one(sql.format(group_id, res_name, action, customer_id))
    #     if row:
    #         return True
    #
    #     return False


    # # give customer_id to check if the given user has "customer admin" group
    # def has_admin_groups(self, user_id, customer_id=None):
    #
    #     if customer_id:
    #         res_name = CUSTOMER_ADMIN_PERMISSION['resource']
    #         action = CUSTOMER_ADMIN_PERMISSION['action']
    #     else:
    #         res_name = ADMIN_PERMISSION['resource']
    #         action = ADMIN_PERMISSION['action']
    #
    #     sql = """
    #         select g.*
    #         from `Group` g
    #         inner join Group_User gu on gu.group_id = g.id
    #         inner join Role r on g.role_id = r.id
    #         inner join Role_Function rf on rf.role_id = r.id
    #         inner join Function f on rf.function_id = f.id
    #         inner join Function_Permission fp on fp.function_id = f.id
    #         inner join Permission p on fp.permission_id = p.id
    #         where gu.user_id = '{}' and p.res_name = '{}' and p.action = '{}'
    #     """
    #     if customer_id:
    #         sql += " and p.value = {}".format(customer_id)
    #
    #     return self.find_by_sql(sql.format(user_id, res_name, action))


    def find(self, params, customer_id=None, user_id=None):

        # user 'left' join to get the group even when there is no user in that group
        sql = """
            select distinct g.*
            from `Group` g
            left join Group_User gu on g.id = gu.group_id
            where 1 = 1
        """

        if params:
            if 'user_id' in params or 'group_id' in params:
                where_clause = self.get_where_clause(params, table_abbr="gu")
                sql += " and {}".format(where_clause)
            else:
                where_clause = self.get_where_clause(params, table_abbr="g")
                sql += " and {}".format(where_clause)
        # else:
        #     raise Exception("no params given")

        if customer_id:
            sql += """
                and g.id in (select id
                	from `Group`
                	where customer_id = '{}')
            """.format(customer_id)

        elif user_id:
            sql += """
                and gu.group_id in (select group_id
                	from Group_User
                	where user_id = '{}')
            """.format(user_id)

        return self.find_by_sql(sql)


    def find_by_ids(self, group_ids, customer_id=None, user_id=None):

        sql = """
            select distinct *
            from `Group`
            left join Group_User gu on g.id = gu.group_id
            where id = in ('{}')
        """.format("','".join(group_ids))

        if customer_id:
            sql += """
                and g.id in (select id
                	from `Group`
                	where customer_id = '{}')
            """.format(customer_id)

        elif user_id:
            sql += """
                and gu.group_id in (select group_id
                	from Group_User
                	where user_id = '{}')
            """.format(user_id)

        return self.find_one(sql)


    def find_by_user_ids(self, user_ids, customer_id=None, user_id=None):
        sql = """
            select distinct gu.user_id, g.*
            from `Group` g
            left join Group_User gu on g.id = gu.group_id
            where gu.user_id in ('{}')
        """.format("','".join(user_ids))

        if customer_id:
            sql += """
                and g.id in (select id
                	from `Group`
                	where customer_id = '{}')
            """.format(customer_id)

        elif user_id:
            sql += """
                and gu.group_id in (select group_id
                	from Group_User
                	where user_id = '{}')
            """.format(user_id)

        return self.find_one(sql)
