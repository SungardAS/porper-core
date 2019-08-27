
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class RoleFunction(Resource):

    def __init__(self, connection=None):
        Resource.__init__(self, connection)
        self.table_name = "`Role_Function`"


    def delete(self, role_id=None, function_id=None):
        sql = "DELETE FROM {}".format(self.table_name)
        if role_id and function_id:
            where_clause = "role_id = '{}' AND function_id = '{}'".format(role_id, function_id)
        elif role_id:
            where_clause = "role_id = '{}'".format(role_id)
        elif function_id:
            where_clause = "function_id = '{}'".format(function_id)
        else:
            raise Exception("either role_id or function_id must be given")
        sql += " WHERE {}".format(where_clause)
        return self.execute(sql)
