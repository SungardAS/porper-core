
import sys
sys.path.insert(0, r'../..')
from models.connection import connection
from models.permission import Permission
permission = Permission(connection)

print permission.create({'user_id':'49d8bc68-f57e-11e3-ba1d-005056ba0d15', 'resource':'res-a', 'action':'act-a', 'value':'val-a', 'condition':'cond-a', 'role_id':''})
print permission.create({'user_id':'', 'resource':'res', 'action':'act-r', 'value':'val-r', 'condition':'', 'role_id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
print permission.find({'user_id':'49d8bc68-f57e-11e3-ba1d-005056ba0d15', 'resource':'account', 'action':'', 'value':'', 'condition':'', 'role_id':'', 'all':True})
print permission.find({'user_id':'', 'resource':'res', 'action':'act-r', 'value':'', 'condition':'', 'role_id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
print permission.delete({'user_id':'49d8bc68-f57e-11e3-ba1d-005056ba0d15', 'resource':'res-a', 'action':'act-a', 'value':'val-a', 'condition':'cond-a', 'role_id':''})
print permission.delete({'user_id':'', 'resource':'res', 'action':'act-r', 'value':'val-r', 'condition':'', 'role_id':'3867c370-552f-43b8-bed9-6aa00ffc41b4'})
