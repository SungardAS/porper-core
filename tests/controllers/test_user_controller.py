
#region = 'us-east-1'
#connection = None

region = None
import sys
sys.path.insert(0, r'..')
from models.connection import connection

from user_controller import UserController
user_controller = UserController(region, connection)

#access_token = '091e304b-1a3f-4406-ac3a-cf8afd8cd647';  # alex.ough
#access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5';    # cloud_test_user
#params = {};
#role_id = '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a';   # public
role_id = '3867c370-552f-43b8-bed9-6aa00ffc41b4';   # Awesome Role
access_token = '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5';    # cloud_test_user
params = {'role_id': role_id};
user_controller.find_all(access_token, params)
