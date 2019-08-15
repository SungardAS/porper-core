
from __future__ import print_function # Python 2/3 compatibility
import os
import uuid
import pymysql
import aws_lambda_logging
import logging

class Resource:

    def __init__(self, connection=None):
        if connection is None:
            host = os.environ.get('MYSQL_HOST')
            username = os.environ.get('MYSQL_USER')
            password = os.environ.get('MYSQL_PASSWORD')
            database = os.environ.get('MYSQL_DATABASE')
            self.connection = pymysql.connect(host, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor)
            print("!!!!!!!!!!new connection created")
        else:
            self.connection = connection
        self.table_name = None

        self.logger = logging.getLogger()
        loglevel = "INFO"
        logging.basicConfig(level=logging.ERROR)
        aws_lambda_logging.setup(level=loglevel)


    def __extract(self, params):
        keys = list(params.keys())
        vals = list(params.values())
        for idx, val in enumerate(vals):
            if isinstance(val, str):
                val = "'{}'".format(val)
                vals[idx] = val
        return (keys, vals)


    def create(self, params):
        if 'id' not in params:
            params['id'] = str(uuid.uuid4())
        (keys, vals) = self.__extract(params)
        sql = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, ",".join(keys), ",".join(vals))
        self.execute(sql)
        return params


    def update(self, params):
        id = params['id']
        (keys, vals) = self.__extract(params)
        sets = []
        for idx, key in enumerate(keys):
            if key == 'id':
                continue
            sets.append("{} = {}".format(key, vals[idx]))
        sql = "UPDATE {} SET {} WHERE id = '{}'".format(self.table_name, ", ".join(sets), id)
        if self.execute(sql):
            return params


    def delete(self, id):
        sql = "DELETE FROM {} WHERE id = '{}'".format(self.table_name, id)
        return self.execute(sql)


    def execute(self, sql):
        sql = sql.replace('\n', ' ')
        self.logger.info(f"SQL:{sql}")
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        return True


    def get_where_clause(self, params, table_abbr=None):
        if table_abbr is None:
            table_abbr = ""
        else:
            table_abbr = '{}.'.format(table_abbr)
        wheres = []
        (keys, vals) = self.__extract(params)
        for idx, key in enumerate(keys):
            wheres.append('{}{} = {}'.format(table_abbr, key, vals[idx]))
        return " and ".join(wheres)


    def find_by_id(self, id, colstr=None):
        if not colstr:
            colstr = "*"
        sql = "SELECT {} FROM {} WHERE id = '{}'".format(colstr, self.table_name, id)
        return self.find_one(sql)


    def find_simple(self, params):
        colstr = "*"
        sql = "SELECT {} FROM {}".format(colstr, self.table_name)
        if not params:
            return self.find_by_sql(sql)
        where_clause = self.get_where_clause(params)
        sql += " WHERE {}".format(where_clause)
        return self.find_by_sql(sql)


    def find_by_sql(self, sql):
        sql = sql.replace('\n', ' ')
        self.logger.info(f"SQL:{sql}")
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        return rows


    def find_one(self, sql):
        sql = sql.replace('\n', ' ')
        self.logger.info(f"SQL:{sql}")
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
        return row


    def commit(self):
        self.connection.commit()


    def rollback(self):
        self.connection.rollback()
