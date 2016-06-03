
import os
import boto3

class Dynamodb():

    def __init__(self, region):
        self.region = region;
        self.dynamodb = boto3.client(
            'dynamodb',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),
            region_name=region
        )

    def save(self, item):
        self.dynamodb.put_item(TableName=self.table_name, Item=item)

    def find_all(self, **kwargs):
        res = self.dynamodb.scan(TableName=self.table_name, **kwargs)
        return self.__build_data(res)

    def find_batch(self, **kwargs):
        res = self.dynamodb.batch_get_item(**kwargs)
        return self.__build_batch_data(res)

    def find(self, **kwargs):
        res = self.dynamodb.query(TableName=self.table_name, **kwargs)
        return self.__build_data(res)

    def remove(self, **kwargs):
        return self.dynamodb.delete_item(TableName=self.table_name, **kwargs)

    def __build_data(self, res):
        items = []
        for item in res['Items']:
            row = {}
            for key in item.keys():
                row[key] = item[key].values()[0]
            items.append(row)
        return items

    def __build_batch_data(self, res):
        items = []
        for item in res['Responses'][self.table_name]:
            row = {}
            for key in item.keys():
                row[key] = item[key].values()[0]
            items.append(row)
        return items
