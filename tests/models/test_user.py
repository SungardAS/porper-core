
import sys
sys.path.insert(0, r'../..')
from porper.models.connection import mysql_connection
from porper.models.user import User

connection = mysql_connection()
user = User(connection)

print user.find({'role_id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
print user.find({'role_ids':['3867c370-552f-43b8-bed9-6aa00ffc41b4', 'ffffffff-ffff-ffff-ffff-ffffffffffff']})
print user.find({'role_ids':['3867c370-552f-43b8-bed9-6aa00ffc41b4', '435a6417-6c1f-4d7c-87dd-e8f6c0effc7a']})
print user.find({'ids':['b2fc88a6-7253-4850-8d5a-07639b1315aa', 'c8b5dbbe-edd1-4e78-b03a-63b0d779be85']})
print user.find({'ids':[]})
print user.find({})
print user.create({'id': '117043220775623860708',
    'family_name': 'Ough',
    'given_name': 'Alex',
    'email': 'alex.ough@gmail.com'
})

connection.commit()
