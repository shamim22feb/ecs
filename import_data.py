import json
import boto3


table_name = 'data'
with open("data.json",encoding="utf8") as f:
    json_data = json.load(f)
ddb_client = boto3.client("dynamodb", endpoint_url='http://localhost:8000')
response = ddb_client.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'bookID',
            'AttributeType': 'S'
        },
        
    ],
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'bookID',
            'KeyType': 'HASH'
        },
        
    ],
    BillingMode='PAY_PER_REQUEST',
)
import time
time.sleep(10)


ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
with ddb.batch_writer() as batch:
    for item in json_data:
        print(item)
        batch.put_item(Item=item)
