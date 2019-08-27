
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class UserGroup(Resource):

    def __init__(self, connection=None):
        Resource.__init__(self, connection)
        self.table_name = "`Group_User`"


    def find(self, params, customer_id=None, user_id=None):
        sql = """
            select gu.*
            from Group_User gu
            inner join `Group` g on g.id = gu.group_id
            where 1 = 1
        """
        user_ids = []
        group_ids = []
        if 'user_id' in params:
            user_ids.append(params['user_id'])
        if 'group_id' in params:
            group_ids.append(params['group_id'])

        if user_id:
            user_ids.append(user_id)

        if user_ids:
            sql += " and gu.user_id in ('{}')".format("','".join(user_ids))
        if group_ids:
            sql += " and gu.group_id in ('{}')".format("','".join(group_ids))
        if customer_id:
            sql += " and g.customer_id = '{}'".format(customer_id)
        return self.find_by_sql(sql)


    def delete(self, user_id=None, group_id=None):
        sql = "DELETE FROM {}".format(self.table_name)
        if user_id and group_id:
            where_clause = "user_id = '{}' AND group_id = '{}'".format(user_id, group_id)
        elif user_id:
            where_clause = "user_id = '{}'".format(user_id)
        elif group_id:
            where_clause = "group_id = '{}'".format(group_id)
        else:
            raise Exception("either user_id or group_is must be given")
        sql += " WHERE {}".format(where_clause)
        return self.execute(sql)


    """
    def find_by_user_ids(self, user_ids):
        eav = {}
        fe = 'user_id in ('
        for index, user_id in enumerate(user_ids):
            user_id_name = ':user_id_%s' % index
            if index == 0:
                fe += user_id_name
            else:
                fe += ', ' + user_id_name
            eav[user_id_name] = user_id
        fe += ')'
        logger.info(f"fe={fe}")
        logger.info(f"eav={eav}")
        return self.table.scan(
            FilterExpression=fe,
            ExpressionAttributeValues=eav
        )['Items']


    def find_by_group_ids(self, group_ids):
        eav = {}
        fe = 'group_id in ('
        for index, group_id in enumerate(group_ids):
            group_id_name = ':group_id_%s' % index
            if index == 0:
                fe += group_id_name
            else:
                fe += ', ' + group_id_name
            eav[group_id_name] = group_id
        fe += ')'
        logger.info(f"fe={fe}")
        logger.info(f"eav={eav}")
        return self.table.scan(
            FilterExpression=fe,
            ExpressionAttributeValues=eav
        )['Items']


    def find(self, params):

        if not params:
            return self.table.scan()['Items']

        if params.get('user_id') and params.get('group_id'):
            response = self.table.get_item(
                Key={
                    'user_id': params['user_id'],
                    'group_id': params['group_id'],
                }
            )
            if response.get('Item'):
                item = response['Item']
                logger.info(f"GetItem succeeded:{json.dumps(item, indent=4, cls=DecimalEncoder)}")
                return [item]
            else:
                logger.info("GetItem returns no item:")
                return []

        if params.get('user_id'):
            fe = Key('user_id').eq(params['user_id']);
            response = self.table.scan(
                FilterExpression=fe,
            )
            for i in response['Items']:
                logger.info(f"response_items={json.dumps(i, cls=DecimalEncoder)}")
            return response['Items']

        if params.get('group_id'):
            fe = Key('group_id').eq(params['group_id']);
            response = self.table.scan(
                FilterExpression=fe,
            )
            for i in response['Items']:
                logger.info(f"response_items={json.dumps(i, cls=DecimalEncoder)}")
            return response['Items']

        if params.get('email'):
            from user import User
            user = User(self.dynamodb)
            user_items = user.find({'email': params['email']})
            if len(user_items) == 0:    return []
            fe = Key('user_id').eq(user_items[0]['id']);
            response = self.table.scan(
                FilterExpression=fe,
            )
            for i in response['Items']:
                logger.info(f"response_items={json.dumps(i, cls=DecimalEncoder)}")
            return response['Items']

        return []
    """
