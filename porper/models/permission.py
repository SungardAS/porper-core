
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

ALL = "*"
ADMIN_PERMISSION = 'admin'
CUSTOMER_ADMIN_PERMISSION = 'customer admin'
PERMISSION_READ = 'r'
PERMISSION_WRITE = 'w'


class Permission(Resource):

    def __init__(self, connection=None):
        Resource.__init__(self, connection)
        self.table_name = "`Permission`"


    def _generate_id(self, params):
        id = ""
        if params.get('user_id'):
            id = 'u-%s' % params['user_id']
        elif params.get('group_id'):
            id = 'g-%s' % params['group_id']
        return '%s-%s-%s-%s' % (id, params.get('resource'), params.get('action'), params.get('value'))


    def _replace_attr_name(self, params):
        if 'resource' in params:
            params['res_name'] = params['resource']
            del params['resource']
        return params


    def create(self, params):
        params['id'] = self._generate_id(params)
        params = self._replace_attr_name(params)
        return Resource.create(self, params)


    def update(self, params):
        params = self._replace_attr_name(params)
        return Resource.update(self, params)


    """
    def _find_id(self, params):
        if params.get('user_id') is None and params.get('group_id') is None:
            return None
        fe = "action = :action and resource = :resource and #value = :value"
        ean = {'#value': 'value'}
        eav = {':action': params['action'], ':resource': params['resource'], ':value': params['value']}
        if params.get('user_id'):
            fe += " and user_id = :user_id"
            eav[':user_id'] = params['user_id']
        elif params.get('group_id'):
            fe += " and group_id = :group_id"
            eav[':group_id'] = params['group_id']
        response = self.table.scan(
            FilterExpression=fe,
            ExpressionAttributeNames=ean,
            ExpressionAttributeValues=eav
        )
        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))
        if len(response["Items"]) == 0: return None
        else:   return response["Items"][0]['id']
    """


    def find(self, params):
        sql = """
            select distinct p.res_name name, p.action action, p.value value
            from Permission p
            inner join Function_Permission fp on fp.permission_id = p.id
            inner join Function f on fp.function_id = f.id
            inner join Role_Function rf on rf.function_id = f.id
            inner join Role r on r.id = rf.role_id
        """

        if 'user_id' in params:
            sql += """
                inner join `Group` g on g.role_id = r.id
                inner join Group_User gu on gu.group_id = g.id
                inner join User u on u.id = gu.user_id
            """

        sql += """
            where p.group_id is null and p.user_id is null
        """

        if params and 'role_id' in params:
            where_clause = self.get_where_clause({'id': params['role_id']}, table_abbr="r")
            sql += " and {}".format(where_clause)
        elif params and 'function_id' in params:
            where_clause = self.get_where_clause({'id': params['function_id']}, table_abbr="f")
            sql += " and {}".format(where_clause)
        elif params and 'user_id' in params:
            where_clause = self.get_where_clause({'id': params['user_id']}, table_abbr="u")
            sql += " and {}".format(where_clause)
        # else:
        #     raise Exception("no params given")

        return self.find_by_sql(sql)


    # def find(self, params):
    #
    #     sql = "select `id`, `action`, `res_name` resource, `value`, `group_id` from {}".format(self.table_name)
    #
    #     if not params or (not params.get('resource') and not params.get('action') and not params.get('value')):
    #         return self.find(sql.format(self.table_name))
    #
    #     if params:
    #         params = self._replace_attr_name(params)
    #         where_clause = self.get_where_clause(params)
    #         sql += " WHERE {}".format(where_clause)
    #
    #     return self.find_by_sql(sql)
