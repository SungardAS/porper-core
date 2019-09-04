
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class FunctionPermission(Resource):

    def __init__(self, connection=None, loglevel="INFO"):
        Resource.__init__(self, connection, loglevel)
        self.table_name = "`Function_Permission`"


    def delete(self, function_id=None, permission_id=None):
        sql = "DELETE FROM {}".format(self.table_name)
        if function_id and permission_id:
            where_clause = "function_id = '{}' AND permission_id = '{}'".format(function_id, permission_id)
        elif function_id:
            where_clause = "function_id = '{}'".format(function_id)
        elif permission_id:
            where_clause = "permission_id = '{}'".format(permission_id)
        else:
            raise Exception("either function_id or permission_id must be given")
        sql += " WHERE {}".format(where_clause)
        return self.execute(sql)
