
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class Function(Resource):

    def __init__(self, connection=None, loglevel="INFO"):
        Resource.__init__(self, connection, loglevel)
        self.table_name = "`Function`"


    def find(self, params):
        sql = """
            select distinct f.id id, f.name name, p.id p_id,
            p.res_name p_resource_name, p.action p_action, p.value p_resource_id
            from Function f
            left join Function_Permission fp on fp.function_id = f.id
            left join Permission p on p.id = fp.permission_id
        """

        if params:
            sql += """
                inner join Role_Function rf on rf.function_id = f.id
                inner join Role r on r.id = rf.role_id
                inner join `Group` g on g.role_id = r.id
                inner join Group_User gu on gu.group_id = g.id
                inner join User u on u.id = gu.user_id
            """

        sql += " where 1 = 1"

        if params:
            if 'user_id' in params:
                where_clause = self.get_where_clause({"id": params['user_id']}, "u")
                sql += " and {}".format(where_clause)
            else:
                where_clause = self.get_where_clause(params, "f")
                sql += " and {}".format(where_clause)
        # else:
        #     raise Exception("no params given")

        return self.find_by_sql(sql)
