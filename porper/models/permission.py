
from __future__ import print_function # Python 2/3 compatibility
# import json
# import boto3
# from boto3.dynamodb.conditions import Key, Attr
# from botocore.exceptions import ClientError
# from porper.models.decimal_encoder import DecimalEncoder
from porper.models.resource import Resource

ALL = "*"
ADMIN_PERMISSION = 'admin'
CUSTOMER_ADMIN_PERMISSION = 'customeradmin'
PERMISSION_READ = 'r'
PERMISSION_WRITE = 'w'


class Permission(Resource):

    def __init__(self, connection=None, loglevel="INFO"):
        Resource.__init__(self, connection, loglevel)
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
        new_action = params['action']
        del params['action']
        sql = "UPDATE Permission set action = '{}'".format(new_action)
        where_clause = self.get_where_clause(params)
        if where_clause:
            sql += " WHERE {}".format(where_clause)
        return self.execute(sql)


    def delete(self, params):
        params = self._replace_attr_name(params)
        sql = "DELETE FROM Permission"
        where_clause = self.get_where_clause(params)
        if where_clause:
            sql += " WHERE {}".format(where_clause)
        return self.execute(sql)


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


    def find_resource_permissions(self, params, customer_id=None, group_ids=None, user_ids=None):

        sql = """
            select res_name as resource, action, value, customer_id, group_id, user_id
            from Permission
            where 1 = 1
        """

        if params:
            where_clause = self.get_where_clause(params)
            sql += " and {}".format(where_clause)

        if customer_id:
            sql += " and customer_id = '{}'".format(customer_id)
        if group_ids:
            sql += " and group_id in ('{}')".format("','".join(group_ids))
        if user_ids:
            sql += " and user_id in ('{}')".format("','".join(user_ids))

        return self.find_by_sql(sql)


    # def find(self, params):
    #
    #     if not params or (not params.get('resource') and not params.get('action') and not params.get('value')):
    #         return self.table.scan()['Items']
    #
    #     fe = ""
    #     ean = {}
    #     eav = {}
    #     if params.get('resource'):
    #         if fe != "":
    #             fe += " and "
    #         fe += "#resource = :resource"
    #         eav[':resource'] = params['resource']
    #         ean['#resource'] = 'resource'
    #     if params.get('action'):
    #         if fe != "":
    #             fe += " and "
    #         fe += "#action = :action"
    #         eav[':action'] = params['action']
    #         ean['#action'] = 'action'
    #     if params.get('value'):
    #         if fe != "":
    #             fe += " and "
    #         fe += "#value in (:value1, :value2)"
    #         eav[':value1'] = params['value']
    #         eav[':value2'] = ALL
    #         ean['#value'] = 'value'
    #     """if params.get('user_id'):
    #         if params.get('all'):
    #             from user_group import UserGroup
    #             user_group = UserGroup(self.dynamodb)
    #             user_group_items = user_group.find({'user_id': params['user_id']})
    #             group_ids = [ user_group_item['group_id'] for user_group_item in user_group_items ]
    #             if fe != "":
    #                 fe += " and "
    #             if len(group_ids) == 0:
    #                 fe += "#user_id = :user_id"
    #             else:
    #                 fe += "(#user_id = :user_id or group_id in ("
    #                 for index, group_id in enumerate(group_ids):
    #                     group_id_name = ':group_id_%s' % index
    #                     if index == 0:
    #                         fe += group_id_name
    #                     else:
    #                         fe += ', ' + group_id_name
    #                     eav[group_id_name] = group_id
    #                 fe += '))'
    #             eav[':user_id'] = params['user_id']
    #             print(fe)
    #             print(eav)
    #         else:
    #             if fe != "":
    #                 fe += " and "
    #             fe += "#user_id = :user_id"
    #             eav[':user_id'] = params['user_id']
    #         ean['#user_id'] = 'user_id'
    #     elif params.get('group_id'):
    #         if fe != "":
    #             fe += " and "
    #         fe += "#group_id = :group_id"
    #         eav[':group_id'] = params['group_id']
    #         ean['#group_id'] = 'group_id'"""
    #     logger.info(f"{fe}")
    #     logger.info(f"{ean}")
    #     logger.info(f"{eav}")
    #     response = self.table.scan(
    #         FilterExpression=fe,
    #         ExpressionAttributeNames=ean,
    #         ExpressionAttributeValues=eav
    #     )
    #     for i in response['Items']:
    #         logger.info(f"response_items={json.dumps(i, cls=DecimalEncoder)}")
    #     return response["Items"]
