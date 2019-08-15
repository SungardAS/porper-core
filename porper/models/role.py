
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class Role(Resource):

    def __init__(self, connection=None):
        Resource.__init__(self, connection)
        self.table_name = "`Role`"


    def find(self, params, customer_id=None, user_id=None):

        self.logger.info(f"params={params}")

        sql = """
            select distinct r.id role_id, r.name role_name,
            f.id function_id, f.name function_name, p.id permission_id,
            p.res_name resource_name, p.action action, p.value value
            from User u
            inner join Group_User gu on gu.user_id = u.id
            inner join `Group` g on g.id = gu.group_id
            inner join Role r on g.role_id = r.id
            inner join Role_Function rf on rf.role_id = r.id
            inner join Function f on rf.function_id = f.id
            inner join Function_Permission fp on fp.function_id = f.id
            inner join Permission p on fp.permission_id = p.id
            where p.group_id is null and p.user_id is null
        """

        if params:
            where_clause = self.get_where_clause(params, "r")
            if where_clause:
                sql += " and {}".format(where_clause)
        # else:
        #     raise Exception("no params given")

        if customer_id:
            sql += " and g.customer_id = '{}'".format(customer_id)

        if user_id:
            sql += " and gu.user_id = '{}'".format(user_id)

        return self.find_by_sql(sql)
