
region = 'us-east-1'
import sys
sys.path.insert(0, r'../..')
from models.connection import connection

from models.permission import Permission
permission = Permission(connection)
#from models_d.permission import Permission
#permission = Permission(region)

print permission.find({'user_id':'b2fc88a6-7253-4850-8d5a-07639b1315aa', 'resource':'account', 'action':'read', 'value':'089476987273', 'condition':'', 'role_id':''})
print permission.find({'user_id':'49d8bc68-f57e-11e3-ba1d-005056ba0d15', 'resource':'account', 'action':'', 'value':'', 'condition':'', 'role_id':'', 'all':True})
print permission.find({'user_id':'', 'resource':'account', 'action':'', 'value':'', 'condition':'', 'role_id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
print permission.create({'user_id':'49d8bc68-f57e-11e3-ba1d-005056ba0d15', 'resource':'res-a', 'action':'act-a', 'value':'val-a', 'condition':'cond-a', 'role_id':''})
print permission.create({'user_id':'', 'resource':'res', 'action':'act-r', 'value':'val-r', 'condition':'', 'role_id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
print permission.delete({'user_id':'49d8bc68-f57e-11e3-ba1d-005056ba0d15', 'resource':'res-a', 'action':'act-a', 'value':'val-a', 'condition':'', 'role_id':''})
print permission.delete({'user_id':'', 'resource':'res', 'action':'act-r', 'value':'val-r', 'condition':'', 'role_id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
