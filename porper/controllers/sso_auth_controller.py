
import os
import json
import requests

from porper.controllers.auth_controller import AuthController

class SsoAuthController(AuthController):

    def __init__(self, permission_connection):

        AuthController.__init__(self, permission_connection)

        self.host = os.environ.get('SSO_HOST')
        self.username = os.environ.get('SSO_USER')
        self.password = os.environ.get('SSO_PASSWORD')
        self.redirect_uri = os.environ.get('SSO_REDIRECT_URI')

        if not self.host:
            with open('config.json') as data_file:
                sso_info = json.load(data_file)
            #print sso_info
            self.host = sso_info['sso']['host']
            self.username = sso_info['sso']['username']
            self.password = sso_info['sso']['password']
            self.redirect_uri = sso_info['sso']['redirect_uri']

    def authenticate(self, code):

        # get the tokens to see if the given code is valid
        print "code [%s]" % code
        task_url = "service/oauth2/access_token?realm=SungardAS"
        url = "https://%s/%s"%(self.host, task_url)
        client_auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        post_data = {"grant_type": "authorization_code", "code": code, "redirect_uri": self.redirect_uri}
        r = requests.post(url, auth=client_auth, data=post_data, verify=False)
        print r._content
        # {u'access_token': u'ed8f3af2-c28a-439f-aa0c-69e0fd620502', u'id_token': u'eyAidHl...', u'expires_in': 59, u'token_type': u'Bearer', u'scope': u'phone address email cloud openid profile', u'refresh_token': u'8e044a96-2be8-45a5-b9c6-08f118f26f42'}
        tokens = json.loads(r._content)
        if not tokens.get('access_token'):
            raise Exception("unauthorized")

        # now retrieve user info from the returned access_token
        user_info = self.get_user_information(tokens['access_token'])

        # now save the user info & tokens
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        AuthController.authenticate(self,
            user_info['guid'],
            user_info['email'],
            user_info['family_name'],
            user_info['given_name'],
            user_info['displayName'],
            access_token,
            refresh_token)

        # return the access_token if all completed successfully
        user_info['user_id'] = user_info['guid']
        user_info['access_token'] = access_token
        return user_info

    def get_user_information(self, access_token):
        task_url = "service/oauth2/userinfo?realm=SungardAS"
        url = "https://%s/%s"%(self.host, task_url)
        headers = {"Authorization":"Bearer " + access_token}
        r = requests.get(url, headers=headers, verify=False)
        #print r._content
        # {u'family_name': u'Grizzanti', u'userGuid': u'49d8bc68-f57e-11e3-ba1d-005056ba0d15', u'displayName': u'David Grizzanti', u'sub': u'cloud_test_user@sungardas.com', u'roles': [u'UCP-SDE', u'UCP-Administrator', u'UCP-Director', u'UCP-Sungard Administrator'], u'cloudstack_secret_key': u'3wKkwYpikde1KYRtm_YiBesm5_qBds-rOd0lPwsyvZyE8bMrFsuq-eYjeyVHKpH3QNMWB0_j-Br9BmfJ_DUCfw', u'zoneinfo': u'America/New_York', u'company_guid': u'76c6f530-40c1-446d-a5d5-a66e78605149', u'updated_at': u'0', u'applications': [u'UCP'], u'given_name': u'David', u'groups': [], u'cloudstack_api_key': u'P6ORU6HUuBGpDXmVc4yw-rBl-z7lFsl1szqlXWJkurHHmhNSStljTMkWNUI-JUt6LkR0k37y4AAp_DvOKnnQZw', u'guid': u'49d8bc68-f57e-11e3-ba1d-005056ba0d15', u'email': u'cloud_test_user@sungardas.com', u'employeeNumber': u'10032'}
        return json.loads(r._content)
