import json
import boto3
import uuid
import gzip
import bz2
import time

from io import BytesIO
from gzip import GzipFile
from boto3.dynamodb.conditions import Key, Attr


def insert_rtmp_events(headers, rtmp_events):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('table_name')
    for rtmp_event in rtmp_events:
        cloudfront_rtmp_event_id = uuid.uuid4().hex
        log_datetime = int(time.time())
        new_item = {'cloudfront_rtmp_event_id': cloudfront_rtmp_event_id,
                    'log_datetime': log_datetime}
        index = 0
        for header in headers:
            new_item[header] = rtmp_event[index]
            index += 1
        table.put_item(
            Item=new_item
        )
    print('inserted successfully')


def lambda_handler(event, context):
    # Event
    # Connection to s3
    print(event)
    s3 = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    object_readed = obj['Body'].read()
    # Decompress
    bytestream = BytesIO(object_readed)
    content = GzipFile(None, 'rb', fileobj=bytestream).read().decode('utf-8')
    # Getting lines from file
    lines = content.split('\n')
    index = 0
    headers = []
    rtmp_events = []
    # Ignore first and last line
    for line in lines[1:len(headers)-1]:
        if index == 0:
            headers = line.split(" ")
        else:
            line = line.split("\t")
            rtmp_events.append(line)
        index += 1
    # ignore first header & inserting to db
    insert_rtmp_events(headers[1:len(headers)], rtmp_events)
    # delete file
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket_name, file_key)
    obj.delete()

    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }
