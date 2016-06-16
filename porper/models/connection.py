import os
import json

host = os.environ.get('MYSQL_HOST')
username = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')
port = os.environ.get('MYSQL_PORT')

if not host:
    with open('config.json') as data_file:
        connection_info = json.load(data_file)
    #print connection_info
    host = connection_info['mysql']['host']
    username = connection_info['mysql']['username']
    password = connection_info['mysql']['password']
    database = connection_info['mysql']['database']
    port = connection_info['mysql']['port']

import pymysql
connection = pymysql.connect(host, user=username, passwd=password, db=database)
