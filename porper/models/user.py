
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class User(Resource):

    def __init__(self, connection=None):
        Resource.__init__(self, connection)
        self.table_name = "`User`"


    def find(self, params, customer_id=None, user_id=None):
        sql = """
            select distinct u.*, g.id as group_id, g.name as group_name, g.customer_id, g.role_id
            from User u
            inner join Group_User gu on u.id = gu.user_id
            inner join `Group` g on g.id = gu.group_id
            where 1 = 1
        """

        if params:
            where_clause = self.get_where_clause(params, table_abbr="gu")
            sql += " and {}".format(where_clause)
        # else:
        #     raise Exception("no params given")

        if customer_id:
            sql += """
                and gu.group_id in (select id
                	from `Group`
                	where customer_id = '{}')
            """.format(customer_id)

        if user_id:
            sql += """
                and gu.group_id in
                (select group_id from Group_User
                    and gu.user_id = '{}')
            """.format(user_id)

        return self.find_by_sql(sql)


    def find_by_ids(self, user_ids, customer_id=None, user_id=None):
        sql = """
            select distinct u.*, g.id as group_id, g.name as group_name, g.customer_id, g.role_id
            from User u
            inner join Group_User gu on u.id = gu.user_id
            inner join `Group` g on g.id = gu.group_id
            where u.id in ({})
        """.format("','".join(user_ids))

        if customer_id:
            sql += """
                and gu.group_id in (select id
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


    # def find(self, group_id, user_id=None):
    #     sql = """
    #         select u.*
    #         from User u
    #         inner join Group_User gu on u.id = gu.user_id
    #     """
    #     if user_id:
    #         where_clause = """
    #             gu.group_id in
    #             (select group_id from Group_User
    #                 where group_id = '{}'
    #                 and gu.user_id = '{}')
    #         """.format(group_id, user_id)
    #     else:
    #         where_clause = "gu.group_id = '{}'".format(group_id)
    #     sql += " WHERE {}".format(where_clause)
    #     return self.find_by_sql(sql)
