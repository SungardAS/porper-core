
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class Function(Resource):

    def __init__(self, connection=None):
        Resource.__init__(self, connection)
        self.table_name = "`Function`"


    def find(self, params):
        sql = """
            select distinct f.id id, f.name name, p.id p_id,
            p.res_name p_resource_name, p.action p_action, p.value p_resource_id
            from User u
            inner join Group_User gu on gu.user_id = u.id
            inner join `Group` g on g.id = gu.group_id
            inner join Role r on g.role_id = r.id
            inner join Role_Function rf on rf.role_id = r.id
            inner join Function f on rf.function_id = f.id
            inner join Function_Permission fp on fp.function_id = f.id
            inner join Permission p on fp.permission_id = p.id
            where 1 = 1
        """

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
