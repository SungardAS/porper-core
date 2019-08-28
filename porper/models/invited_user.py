
from __future__ import print_function # Python 2/3 compatibility
from porper.models.resource import Resource

class InvitedUser(Resource):

    def __init__(self, connection=None):
        Resource.__init__(self, connection)
        self.table_name = "`InvitedUser`"
        self.INVITED = 'invited'
        self.REGISTERED = 'registered'
        self.CANCELLED = 'cancelled'
        self.DELETED = 'deleted'

        self.permission_name = 'invite'


    def find(self, params, customer_id=None, user_id=None):

        self.logger.info(f"params={params}")

        # use 'left' join with Group_User
        sql = """
            select distinct g.customer_id customer_id, iv.id, iv.email, iv.auth_type, iv.group_id,
                iv.invited_at, iv.invited_by, iv.state, u.email invited_by_email, g.name group_name
            from InvitedUser iv
            inner join User u on u.id = iv.invited_by
            inner join `Group` g on g.id = iv.group_id
            left join Group_User gu on g.id = gu.group_id
            where 1 = 1
        """

        if params:
            where_clause = self.get_where_clause(params, "iv")
            sql += " and {}".format(where_clause)
        # else:
        #     raise Exception("no params given")

        if customer_id:
            sql += """
                and g.id in (select id
                	from `Group`
                	where customer_id = '{}')
            """.format(customer_id)

        elif user_id:
            sql += """
                and gu.group_id in (select group_id
                	from Group_User
                	where user_id = '{}')
            """.format(user_id)

        return self.find_by_sql(sql)


    def update_state(self, email, auth_type, state):
        sql = "UPDATE {} SET state = '{}' WHERE email = '{}' AND auth_type = '{}'".format(self.table_name, state, email, auth_type)
        return self.execute(sql)
