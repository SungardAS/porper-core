import os
import json

host = os.environ.get('MYSQL_HOST')
username = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')
port = os.environ.get('MYSQL_PORT')

if not host:
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    with open(cur_dir + '/config.json') as data_file:
        connection_info = json.load(data_file)
    #print connection_info
    host = connection_info['host']
    username = connection_info['username']
    password = connection_info['password']
    database = connection_info['database']
    port = connection_info['port']

import pymysql
connection = pymysql.connect(host, user=username, passwd=password, db=database)
