
import sys
sys.path.insert(0, r'../..')
from porper.models.connection import mysql_connection
from porper.controllers.role_controller import RoleController

connection = mysql_connection()
role_controller = RoleController(connection)

#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647'   # alex.ough's token
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'    # cloud_test_user's token
print role_controller.find_all(access_token)

connection.commit()
