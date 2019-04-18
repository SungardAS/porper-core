
import os
import json
import uuid
import boto3
from porper.controllers.auth_controller import AuthController

class CognitoAuthController(AuthController):

    def __init__(self, permission_connection):

        AuthController.__init__(self, permission_connection)

        self.client = boto3.client('cognito-idp')


    def authenticate(self, params):

        access_token = params['access_token']

        # get the tokens to see if the given code is valid
        print("access_token [{}]".format(access_token))
        response = self.client.get_user(AccessToken=access_token)
        print(response)
        """{
            'Username': 'string',
            'UserAttributes': [
                {
                    'Name': 'string',
                    'Value': 'string'
                },
            ],
            'MFAOptions': [
                {
                    'DeliveryMedium': 'SMS'|'EMAIL',
                    'AttributeName': 'string'
                },
            ],
            'PreferredMfaSetting': 'string',
            'UserMFASettingList': [
                'string',
            ]
        }"""
        if not response.get('Username'):
            raise Exception("unauthorized")

        # now save the user info & tokens
        auth_params = {
            'user_id': response.get('Username'),
            'email': response.get('Username'),
            'family_name': "",
            'given_name': "",
            'name': "",
            'auth_type': 'cognito',
            'access_token': access_token,
            'refresh_token': access_token
        }
        AuthController.authenticate(self, auth_params)

        # return the access_token if all completed successfully
        user_info['user_id'] = user_info['sub']
        user_info['access_token'] = access_token
        user_info['groups'] = AuthController.find_groups(self, auth_params['user_id'])
        return user_info
