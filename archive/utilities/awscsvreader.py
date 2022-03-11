import boto3
import csv

def csv_reader(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    s3_resource = boto3.resource('s3')
    s3_object = s3_resource.Object(bucket, key)

    data = s3_object.get()['Body'].read().decode('utf-8').splitlines()
    lines = csv.reader(data)
    headers = next(lines)
    print('headers: %s' %(headers))
    for line in lines:
        #print complete line
        print(line)
        #print index wise
        print(line[0], line[1])
