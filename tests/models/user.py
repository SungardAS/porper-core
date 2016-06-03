
region = 'us-east-1'
from connection import connection

from user import User
#user = User(connection)
user = User(region)

user.find({'role_id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
user.find({'role_ids':['3867c370-552f-43b8-bed9-6aa00ffc41b4', 'ffffffff-ffff-ffff-ffff-ffffffffffff']})
user.find({'role_ids':['3867c370-552f-43b8-bed9-6aa00ffc41b4', '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a']})
user.find({'ids':['b2fc88a6-7253-4850-8d5a-07639b1315aa', 'c8b5dbbe-edd1-4e78-b03a-63b0d779be85']})
user.find({'ids':[]})
user.find({})
user.create({'id': '117043220775623860708',
    'family_name': 'Ough',
    'given_name': 'Alex',
    'email': 'alex.ough@gmail.com'
})
