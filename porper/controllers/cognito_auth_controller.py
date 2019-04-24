
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
                'Username': '4de37a8c-c2c0-4cc4-9fbb-c578139fb861',
                'UserAttributes': [
                    {'Name': 'sub', 'Value': '4de37a8c-c2c0-4cc4-9fbb-c578139fb861'},
                    {'Name': 'given_name', 'Value': 'TestA'},
                    {'Name': 'family_name', 'Value': 'TestB'},
                    {'Name': 'email', 'Value': 'abay.radhakrishnan@sungardas.com'}
                ],
                'ResponseMetadata': {
                    'RequestId': '06ecec11-6187-11e9-aad6-45ac547975c8',
                    'HTTPStatusCode': 200,
                    'HTTPHeaders': {
                        'date': 'Thu, 18 Apr 2019 03:06:57 GMT',
                        'content-type': 'application/x-amz-json-1.1',
                        'content-length': '269',
                        'connection': 'keep-alive',
                        'x-amzn-requestid': '06ecec11-6187-11e9-aad6-45ac547975c8'
                    },
                    'RetryAttempts': 0
                }
            }
        """
        if not response.get('Username'):
            raise Exception("unauthorized")

        # now save the user info & tokens
        user_id = response.get('Username')
        email = [attr for attr in response.get('UserAttributes') if attr['Name'] == 'email'][0]['Value']
        family_name = [attr for attr in response.get('UserAttributes') if attr['Name'] == 'family_name'][0]['Value']
        given_name = [attr for attr in response.get('UserAttributes') if attr['Name'] == 'given_name'][0]['Value']

        auth_params = {
            'user_id': user_id,
            'email': email,
            'family_name': family_name,
            'given_name': given_name,
            'auth_type': 'cognito',
            'access_token': access_token,
            'refresh_token': access_token
        }
        auth_params['name'] = "{} {}".format(given_name, family_name)
        AuthController.authenticate(self, auth_params)

        # return the access_token if all completed successfully
        user_info['user_id'] = user_id
        user_info['access_token'] = access_token
        user_info['groups'] = AuthController.find_groups(self, user_id])
        return user_info
