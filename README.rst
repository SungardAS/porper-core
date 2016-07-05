Portable Permission Controller
==============================

This is a library to provide the permission control on resources in serverless environment.

When implementing applications using existing frameworks, you can manage user permissions on resources using the module they provide,
but they are not available when you implement applications using serverless computing like AWS Lambda.

This is a very simple permission control library to manage user permissions based on their privileges.


==========================================================================================
How to provide related info
==========================================================================================

export MYSQL_HOST=$db_host
export MYSQL_USER=$db_user
export MYSQL_PASSWORD=$db_password
export MYSQL_DATABASE=$db_name
export MYSQL_PORT=3306

export GOOGLE_TOKENINFO_ENDPOINT=https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=

export SSO_HOST=$sso_host
export SSO_USER=$sso_user
export SSO_PASSWORD=$sso_password
export SSO_REDIRECT_URI=$redirect_uri

export GITHUB_AUTH_ENDPOINT=https://github.com/login/oauth
export GITHUB_API_ENDPOINT=https://api.github.com
export GITHUB_CLIENT_ID=$client_id
export GITHUB_CLIENT_SECRET=$secret_id
export GITHUB_REDIRECT_URI=$redirect_uri

config.json
{
  "mysql": {
    "host": "$db_host",
    "username": "$db_user",
    "password": "$db_password",
    "database": "$db_name",
    "port": 3306
  },
  "sso": {
    "host": "$sso_host",
    "username": "$sso_user",
    "password": "$sso_password",
    "redirect_uri": "$redirect_uri"
  },
  "google": {
    "tokeninfo_endpoint": "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="
  },
  "github": {
    "auth_endpoint": "https://github.com/login/oauth",
    "api_endpoint": "https://api.github.com",
    "client_id": "$client_id",
    "client_secret": "$secret_id",
    "redirect_uri": "$redirect_uri"
  }
}


==========================================================================================
how to populate mysql database
==========================================================================================

After creating the target database
$ mysql -h db_host -u db_user -p db_name < porper_initial.sql



==========================================================================================
how to get mysql connection
==========================================================================================

from porper.models.connection import mysql_connection

# there are 3 ways to get connection
connection = mysql_connection()






==========================================================================================
how to authenticate
==========================================================================================

from porper.models.connection import mysql_connection
from porper.controllers.sso_auth_controller import SsoAuthController
from porper.controllers.google_auth_controller import GoogleAuthController
from porper.controllers.github_auth_controller import GithubAuthController

# get the mysql connection as preferred
# connection = mysql_connection()

# SSO server
ssoAuthController = SsoAuthController(connection)
user_info = ssoAuthController.authenticate(code)

# Google Auth
googleAuthController = GoogleAuthController(connection)
user_info = googleAuthController.authenticate(id_token)

# GitHub Auth
# https://developer.github.com/v3/oauth/
githubAuthController = GithubAuthController(connection)
user_info = githubAuthController.authenticate(code, state)


==========================================================================================
how to create roles
==========================================================================================



==========================================================================================
how to assign users to roles
==========================================================================================



==========================================================================================
how to give permissions
==========================================================================================
