
import sys
sys.path.insert(0, r'../..')
from models.connection import connection
from controllers.token_controller import TokenController
token_controller = TokenController(connection)

user_id = 'b2fc88a6-7253-4850-8d5a-07639b1315aa'
print token_controller.save('access1', 'refresh1', user_id)
print token_controller.find('access1')
