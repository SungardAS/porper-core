
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

        code = params['code']
        state = params['state']
        print "code [%s], state [%s]" % (code, state)

        """
        https://slack.com/oauth/authorize?client_id=1234&scope=identity.basic,identity.email
        https://slack.com/api/oauth.access?client_id=1234&client_secret=secretxxxx&code=codexxx
        {"ok":true,"access_token":"xxx","scope":"identify,commands,identity.basic,identity.email","user":{"name":"name","id":"id","email":"email"},"team":{"id":"tid"}}
        """
        access_token_url = "%s/oauth.access" % (self.api_endpoint)
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code
        }
        headers = {"Content-Type":"application/json"}
        r = requests.get(access_token_url, headers=headers, params=payload, verify=False)
        print r
        print r._content

        user_info = json.loads(r._content)

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
            'refresh_token': code
        }
        AuthController.authenticate(self, auth_params)

        # return the access_token if all completed successfully
        user_info['user_id'] = auth_params['user_id']
        user_info['groups'] = AuthController.find_groups(self, auth_params['user_id'])
        return user_info
