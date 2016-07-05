
import sys
sys.path.insert(0, r'../..')
from porper.models.connection import mysql_connection
from porper.controllers.user_role_controller import UserRoleController

connection = mysql_connection()
user_role_controller = UserRoleController(connection)

user_id = 'b2fc88a6-7253-4850-8d5a-07639b1315aa'
print user_role_controller.find_by_user_id(user_id)
role_id = '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a'
print user_role_controller.find_by_role_id(role_id)

connection.commit()
