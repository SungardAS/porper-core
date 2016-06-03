
import sys
sys.path.insert(0, r"..")
from index import permission_handler

context = None
event = {
    "region": "us-east-1",
    "db": "mysql",
    "access_token": "091e304b-1a3f-4406-ac3a-cf8afd8cd647",  # alex.ough"s token
    #"access_token": "3ab4ae48-97fe-4420-8cb1-b1e3c62737f5",    # cloud_test_user"s token
    "resource": "user",
    #"resource": "account",
    "oper": "find_all",
    "params" : {
        "role_id": "ffffffff-ffff-ffff-ffff-ffffffffffff"
    }
}
event["params"]
permission_handler(event, context)

""""params" : {
    #"access_token": "72a8b52a-b1dc-4dd0-ae00-d15037fd42de",
    #"access_token": "0ec85209-df56-4ef9-b5e6-a9971ca4fba7",
    #"user_id": "b2fc88a6-7253-4850-8d5a-07639b1315aa",
    #"role_id": "3867c370-552f-43b8-bed9-6aa00ffc41b4",
    "role_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
    "action": "update"
}"""
"""
"params" : [{
    #"role_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
    "user_id": "b2fc88a6-7253-4850-8d5a-07639b1315aa",
    "resource": "account",
    "value": "*",
    "action": "update",
    "condition": ""
}]"""
