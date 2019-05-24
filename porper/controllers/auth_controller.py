
from porper.controllers.meta_resource_controller import ADMIN_GROUP_ID

class AuthController():

    def __init__(self, permission_connection):
        self.connection = permission_connection
        from porper.controllers.user_controller import UserController
        self.user_controller = UserController(self.connection)
        from porper.controllers.invited_user_controller import InvitedUserController
        self.invited_user_controller = InvitedUserController(self.connection)   
        from porper.controllers.token_controller import TokenController
        self.token_controller = TokenController(self.connection)
        from porper.models.user_group import UserGroup
        self.user_group = UserGroup(self.connection)
        from porper.models.user import User
        self.user = User(self.connection)
        from porper.models.invited_user import InvitedUser
        self.invited_user = InvitedUser(self.connection)
        
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
        print("Before invite")
        invited_user = self.invited_user.find_by_id(email)
        if not invited_user:
           print("Invited user not found")
        else: 
           print("Printing invited user") 
           print(invited_user) 
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

            # find admin user's access_token to replace this user's access_token to create a user
            admin_users = self.user_group.find({'group_id': ADMIN_GROUP_ID})
            if len(admin_users) == 0:
                # this is the first user, so no need to set access_token
                admin_access_token = None
            else:
                admin_access_token = None
                for admin_user in admin_users:
                    try:
                        admin_access_tokens = self.token_controller.find(None, {'user_id': admin_user['user_id']})
                        admin_access_token = admin_access_tokens[0]['access_token']
                        break
                    except:
                        pass
            user_id = self.user_controller.create(admin_access_token, params)

        # now save the tokens
        return self.token_controller.save(access_token, refresh_token, user_id)

    def find_groups(self, user_id):
        from porper.models.user_group import UserGroup
        user_group = UserGroup(self.connection)
        user_groups = user_group.find({'user_id': user_id})
        return user_groups
