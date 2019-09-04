
from __future__ import print_function # Python 2/3 compatibility
import datetime
from porper.models.resource import Resource

class AccessToken(Resource):

    def __init__(self, connection=None, loglevel="INFO"):
        Resource.__init__(self, connection, loglevel)
        self.table_name = "`Token`"


    def create(self, params):
        if 'refreshed_time' not in params:
            params['refreshed_time'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        return Resource.create(self, params)


    def find(self, access_token):
        sql = """
            select * from {}
            where access_token = '{}'
        """
        return self.find_by_sql(sql.format(self.table_name, access_token))


    def find_user(self, access_token):
        sql = """
            select u.* from User u
            inner join Token t on t.user_id = u.id
            where t.access_token = '{}'
        """
        return self.find_one(sql.format(access_token))


    def delete_by_user(self, user_id):
        sql = "DELETE FROM {} WHERE user_id = '{}'".format(self.table_name, user_id)
        return self.execute(sql)


    """
    def find_admin_token(self):

        from porper.models.group import Group
        group = Group(self.dynamodb)
        admin_groups = group.find_admin_groups()
        if not admin_groups:
            print("No admin group found")
            return None
        admin_group_ids = [group['id'] for group in admin_groups]

        from porper.models.user_group import UserGroup
        user_group = UserGroup(self.dynamodb)
        access_tokens = self.find({})
        for access_token in access_tokens:
            token_groups = user_group.find({'user_id': access_token['user_id']})
            if token_groups and token_groups[0]['group_id'] in admin_group_ids:
                print(access_token)
                return access_token['access_token']
    """
