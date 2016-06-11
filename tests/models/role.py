
import sys
sys.path.insert(0, r'../..')
from models.connection import connection
from models.role import Role
role = Role(connection)

print role.find({'id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
print role.find({'ids':['435a6417-6c1f-4d7c-87dd-e8f6c0effc7a', 'ffffffff-ffff-ffff-ffff-ffffffffffff']})
print role.find({'ids':[]})
print role.find({})
print role.create({'id':'333', 'name':'333'})

#print role.create({'id':'ffffffff-ffff-ffff-ffff-ffffffffffff', 'name':'admin'})
#print role.create({'id':'435a6417-6c1f-4d7c-87dd-e8f6c0effc7a', 'name':'public'})
#print role.create({'id':'3867c370-552f-43b8-bed9-6aa00ffc41b4', 'name':'Awesome Role'})
