
import sys
sys.path.insert(0, r'../..')
from models.connection import connection
from models.access_token import AccessToken
access_token = AccessToken(connection)

print access_token.create({'access_token':'access', 'refresh_token':'refresh', 'refreshed_time':'2016-1-1', 'user_id':'b2fc88a6-7253-4850-8d5a-07639b1315aa'})
print access_token.find({'access_token':'access'})
print access_token.update({'access_token':'access', 'refresh_token':'refresh-2', 'refreshed_time':'2016-2-1' })
