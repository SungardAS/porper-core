
"""
http://docs.aws.amazon.com/amazondynamodb/latest/gettingstartedguide/GettingStarted.Python.03.html
"""

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

table = dynamodb.Table('users')

### put item
id = "The Big New Movie"
email = "given.family@sungardas.com"
family_name = "Family"
given_name = "Given"
name = "Given Family"

response = table.put_item(
   Item={
        'id': id,
        'email': email,
        'family_name': family_name,
        'given_name': given_name,
        'name': name
    }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))


### get Item

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

try:
    response = table.get_item(
        Key={
            'id': id
        }
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    item = response['Item']
    print("GetItem succeeded:")
    print(json.dumps(item, indent=4, cls=DecimalEncoder))



### update item

try:
    response = table.update_item(
        Key={
                'id': id
        },
        UpdateExpression="set family_name = :fn, given_name=:gn, #name=:n",
        ExpressionAttributeNames={
            '#name': 'name'
        },
        ExpressionAttributeValues={
            ':fn': "Family2",
            ':gn': "Given2",
            ':n': "Given2 Family2"
        },
        #ConditionExpression="size(info.actors) > :num",
        #ExpressionAttributeValues={
        #    ':num': 3
        #},
        ReturnValues="UPDATED_NEW"
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("UpdateItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))


### delete item

try:
    response = table.delete_item(
        Key={
                'id': id
        },
        #ConditionExpression="family_name <> :val",
        #ExpressionAttributeValues= {
        #    ":val": "Family"
        #}
    )
except ClientError as e:
    if e.response['Error']['Code'] == "ConditionalCheckFailedException":
        print(e.response['Error']['Message'])
    else:
        raise
else:
    print("DeleteItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
