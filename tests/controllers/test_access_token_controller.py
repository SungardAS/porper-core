
#region = 'us-east-1'
#connection = null;

region = None
import sys
sys.path.insert(0, r'..')
from models.connection import connection

from access_token_controller import AccessTokenController
access_token_controller = AccessTokenController(region, connection)

user_id = 'b2fc88a6-7253-4850-8d5a-07639b1315aa'
access_token_controller.save('access1', 'refresh1', user_id)
access_token_controller.find('access1')
