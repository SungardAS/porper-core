
import sys
sys.path.insert(0, r"models/lib")
import pymysql
host = 'porper.cqxu7tlsmwh4.us-east-1.rds.amazonaws.com'
username = 'porper'
password = 'Sungard01'
database = 'porper'
#port = 3306
connection = pymysql.connect(host, user=username, passwd=password, db=database)
