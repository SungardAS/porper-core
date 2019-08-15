
class AuthController():

    def __init__(self, connection=None):
        if not connection:
            host = os.environ.get('MYSQL_HOST')
            username = os.environ.get('MYSQL_USER')
            password = os.environ.get('MYSQL_PASSWORD')
            database = os.environ.get('MYSQL_DATABASE')
            self.connection = pymysql.connect(host, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor)
            print("@@@@@@@@new connection created")
        else:
            self.connection = connection
        # from porper.controllers.user_controller import UserController
        # self.user_controller = UserController(self.connection)
        # from porper.controllers.invited_user_controller import InvitedUserController
        # self.invited_user_controller = InvitedUserController(self.connection)
        # from porper.controllers.token_controller import TokenController
        # self.token_controller = TokenController(self.connection)
        # from porper.models.access_token import AccessToken
        # self.access_token = AccessToken(self.connection)
        from porper.models.user import User
        self.user = User(self.connection)
        from porper.models.user_group import UserGroup
        self.user_group = UserGroup(self.connection)
        from porper.models.invited_user import InvitedUser
        self.invited_user = InvitedUser(self.connection)
        from porper.models.access_token import AccessToken
        self.access_token = AccessToken(self.connection)

    def authenticate(self, params):

        user_id = params['user_id']
        email = params.get('email')
        family_name = params.get('family_name')
        given_name = params.get('given_name')
        name = params.get('name')
        customer_id = params.get('customer_id')
        auth_type = params['auth_type']
        access_token = params['access_token']
        refresh_token = params['refresh_token']
        # print("Before invite")
        # items = self.invited_user.find({'email': params['email'], 'auth_type': params['auth_type']})
        # if items and auth_type == "sso":
        #    customer_id=items[0]['customer_id']
        #    print(customer_id)
        #if not invited_user:
        #   print("Invited user not found")
        #else:
        #   print("Printing invited user")
        #   print(invited_user)
        user = self.user.find_by_id(user_id)
        if not user:
            # create this user
            params = {
                'id': user_id,
                'auth_type': auth_type
            }
            if name:
                params['name'] = name
            if family_name:
                params['family_name'] = family_name
            if given_name:
                params['given_name'] = given_name
            if customer_id:
                params['customer_id'] = customer_id
            if email:
                params['email'] = email.lower()

            # # find admin user's access_token to replace this user's access_token to create a user
            # users = self.user.find({})
            # if not users:
            #     # this is the first user, so no need to set access_token
            #     admin_access_token = None
            # else:
            #     admin_access_token = self.access_token.find_admin_token()
            # user_id = self.user_controller.create(admin_access_token, params)
            user_id = add_user(params)

        # now save the tokens
        # return self.token_controller.save(access_token, refresh_token, user_id)
        self.access_token.create(access_token, refresh_token, user_id)

        user_info = self.user.find_by_id(user_id)
        user_info['user_id'] = user_info['id']
        user_info['access_token'] = access_token
        user_info['groups'] = self.user_group.find_groups([user_id])
        user_info['customer_id'] = user_info['groups'][0]['customer_id']

        return user_info



    def add_user(self, params):

        # if this is the first user, save it as an admin
        users = self.user.find({})
        if len(users) == 0:
            # set this user to the admin
            self.user.create(params)
            from porper.models.group import Group
            group = Group(self.dynamodb)
            admin_groups = group.find_admin_groups()
            if not admin_groups:
                raise Exception("No admin group found")
            self.user_group.create({
                'user_id': params['id'],
                'group_id': admin_groups[0]['id']
            })
            return params['id']

        # # add the given user to the specified group
        # if params.get("group_id"):
        #     return self.user_group.create(
        #         {
        #             "user_id": params['id'],
        #             "group_id": params["group_id"]
        #         }
        #     )
        #
        # # find if the given user already exists
        # rows = self.user.find({"email": params['email'], "auth_type": params['auth_type']})
        # if len(rows) > 0:
        #     print('already exists')
        #     return rows[0]['id']

        # find if the given user is already invited
        invited_users = self.invited_user.find({'email':params['email'], 'auth_type':params['auth_type']})
        if len(invited_users) == 0:
            raise Exception("Please invite this user first")

        # add user_group_rel first to check the permission
        # if the current user is not admin and group admin, it will fail

        # check if the current user is the admin of the invited user's group
        #if current_user['level'] != self.USER_LEVEL_ADMIN and not self.is_group_admin(current_user['user_id'], invited_users[0]['group_id']):
        #    raise Exception("Not permitted")

        # create a user and add it to the specified group
        self.user.create({
            'id': params['id'],
            'email': params['email'],
            'auth_type': params['auth_type'],
            'name': params['name'],
            'family_name': params['family_name'],
            'given_name': params['given_name'],
            'customer_id': params['customer_id']
        })
        self.user_group.create({
            'user_id': params['id'],
            'group_id': invited_users[0]['group_id']
        })
        self.invited_user.update_state({
            'email':params['email'],
            'auth_type':params['auth_type'],
            'state':self.invited_user.REGISTERED
        })
        return params['id']


    # def find_groups(self, user_id):
    #     from porper.models.user_group import UserGroup
    #     user_group = UserGroup(self.connection)
    #     user_groups = user_group.find({'user_id': user_id})
    #     return user_groups
