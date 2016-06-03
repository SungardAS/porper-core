
import pymysql
host = ''
username = ''
password = ''
database = ''
#port = 3306
connection = pymysql.connect(host, user=username, passwd=password, db=database)
