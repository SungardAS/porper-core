
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))

import json
with open(cur_dir + '/config.json') as data_file:
    connection_info = json.load(data_file)
#print connection_info

import sys
sys.path.insert(0, r"models/lib")
import pymysql
host = connection_info['host']
username = connection_info['username']
password = connection_info['password']
database = connection_info['database']
port = connection_info['port']
connection = pymysql.connect(host, user=username, passwd=password, db=database)
