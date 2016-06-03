
region = 'us-east-1'
from connection import connection

from access_token import AccessToken
#token = Token(connection)
token = Token(region)

token.find({'access_token':'access'})
token.create({'access_token':'access', 'refresh_token':'refresh', 'refreshed_time':'2016-1-1', 'user_id':'b2fc88a6-7253-4850-8d5a-07639b1315aa'})
token.update({'access_token':'access', 'refreshed_time':'2016-2-1'})
