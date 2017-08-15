
import os
import json
import requests
from porper.controllers.auth_controller import AuthController

class SlackAuthController(AuthController):

    def __init__(self, permission_connection):

        AuthController.__init__(self, permission_connection)

        self.api_endpoint = os.environ.get('SLACK_API_ENDPOINT')
        self.client_id = os.environ.get('SLACK_CLIENT_ID')
        self.client_secret = os.environ.get('SLACK_CLIENT_SECRET')

    def authenticate(self, params):
        code = params.get('code')
        state = params.get('state')
        access_token = params.get('access_token')
        print "code [%s], state [%s], access_token [%s]" % (code, state, access_token)
        if access_token:
            return self.validate(access_token)
        else:
            return self.login(code, state)

    def login(self, code, state):

        """
        https://slack.com/oauth/authorize?client_id=1234&scope=identity.basic,identity.email
        https://slack.com/api/oauth.access?client_id=1234&client_secret=secretxxxx&code=codexxx
        {"ok":true,"access_token":"xxx","scope":"identify,commands,identity.basic,identity.email","user":{"name":"name","id":"id","email":"email"},"team":{"id":"tid"}}
        """
        api_url = "%s/oauth.access" % (self.api_endpoint)
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code
        }
        headers = {"Content-Type":"application/json"}
        r = requests.get(api_url, headers=headers, params=payload, verify=False)
        print r
        print r._content
        user_info = json.loads(r._content)
        user_info['refresh_token'] = code
        return self.save(user_info)


    def validate(self, access_token):

        # https://slack.com/api/users.identity?token=xoxp-1111827393-16111519414-20367011469-5f89a31i07
        api_url = "%s/users.identity" % (self.api_endpoint)
        payload = {
            "token": access_token
        }
        headers = {"Content-Type":"application/json"}
        r = requests.get(api_url, headers=headers, params=payload, verify=False)
        print r
        print r._content
        """
        {
            "ok": true,
            "user": {
                "name": "Alex Ough",
                "id": "U2074A9SS",
                "email": "alex.ough@sungardas.com"
            },
            "team": {
                "id": "T0H6QL4DD"
            }
        }
        """
        user_info = json.loads(r._content)
        user_info['access_token'] = access_token
        user_info['refresh_token'] = access_token
        return self.save(user_info)


    def save(self, user_info):

        splitted = user_info['user']['name'].split(' ')
        first_name = " ".join(splitted[:len(splitted)-1])
        last_name = splitted[len(splitted)-1]

        # now save the user info & tokens
        auth_params = {
            'user_id': '%s-%s' % (user_info['team']['id'], user_info['user']['id']),
            'email': user_info['user']['email'],
            'family_name': last_name,
            'given_name': first_name,
            'name': user_info['user']['name'],
            'auth_type': 'slack',
            'slack_team_id': user_info['team']['id'],
            #'slack_bot_name': bot_name,
            'access_token': user_info['access_token'],
            'refresh_token': user_info['refresh_token']
        }
        AuthController.authenticate(self, auth_params)

        # return the access_token if all completed successfully
        user_info['user_id'] = auth_params['user_id']
        user_info['groups'] = AuthController.find_groups(self, auth_params['user_id'])
        return user_info
