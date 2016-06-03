
import sys
sys.path.insert(0, r'..')
from index import permission_handler

context = None
event = {
    'region': 'us-east-1',
    'access_token': '091e304b-1a3f-4406-ac3a-cf8afd8cd647',  # alex.ough's token
    #'access_token': '3ab4ae48-97fe-4420-8cb1-b1e3c62737f5',   # cloud_test_user's token
    'db': 'mysql',
    'resource': 'permission',
    'oper': 'find_all',
    "params" : {
        #'user_id': 'b2fc88a6-7253-4850-8d5a-07639b1315aa',
        #'user_id': '49d8bc68-f57e-11e3-ba1d-005056ba0d15',
        #'user_id': 'c8b5dbbe-edd1-4e78-b03a-63b0d779be85',  # alex_role
        #'role_id': '3867c370-552f-43b8-bed9-6aa00ffc41b4', # Awesome Role
        #'action': 'read',
        "role_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
        "resource": "service",
        #"value": "*",
        "action": "update",
        #"condition": ""
    }
}
permission_handler(event, context)
