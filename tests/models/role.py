
region = 'us-east-1'
from connection import connection

from role import Role
#role = Role(connection)
role = Role(region)

role.find({'id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
role.find({'ids':['435a6417-6c1f-4d7c-87dd-e8f6c0effc7a', 'ffffffff-ffff-ffff-ffff-ffffffffffff']})
role.find({'ids':[]})
role.find({})
role.create({'id':'333', 'name':'333'})

#role.create({'id':'ffffffff-ffff-ffff-ffff-ffffffffffff', 'name':'admin'})
#role.create({'id':'435a6417-6c1f-4d7c-87dd-e8f6c0effc7a', 'name':'public'})
#role.create({'id':'3867c370-552f-43b8-bed9-6aa00ffc41b4', 'name':'Awesome Role'})
