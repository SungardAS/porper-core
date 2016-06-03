
#region = 'us-east-1'
#connection = None

region = None
import sys
sys.path.insert(0, r'..')
from models.connection import connection

from role_controller import RoleController
role_controller = RoleController(region, connection)

#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647'   # alex.ough's token
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5'    # cloud_test_user's token
role_controller.find_all(access_token)
