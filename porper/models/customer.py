
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class Customer(Resource):

    def __init__(self, connection=None, loglevel="INFO"):
        Resource.__init__(self, connection, loglevel)
        self.table_name = "`Customer`"


    def find(self, params):
        sql = """
            select distinct c.*
            from Customer c
            inner join `Group` g on g.customer_id = c.id
            inner join Group_User gu on gu.group_id = g.id
            where 1 = 1
        """

        if params:
            if 'user_id' in params:
                where_clause = self.get_where_clause(params, "gu")
                sql += " and {}".format(where_clause)
            else:
                where_clause = self.get_where_clause(params, "c")
                sql += " and {}".format(where_clause)
        # else:
        #     raise Exception("no params given")

        return self.find_by_sql(sql)
