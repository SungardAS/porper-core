
#region = 'us-east-1'
#connection = null;

region = None
import sys
sys.path.insert(0, r'..')
from models.connection import connection

from user_role_controller import UserRoleController
user_role_controller = UserRoleController(region, connection)

user_id = 'b2fc88a6-7253-4850-8d5a-07639b1315aa'
user_role_controller.find_by_user_id(user_id)
role_id = '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a'
user_role_controller.find_by_role_id(role_id)
