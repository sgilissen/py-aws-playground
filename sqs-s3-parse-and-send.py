"""
sqs-s3-parse-and-send.py
Fetch CSV data from S3, format and send to SQS Queue
"""
import boto3
from botocore.exceptions import ClientError
import datetime
import csv
import codecs
import json
from pprint import pprint

# Define global AWS clients
s3_resource = boto3.resource('s3')
s3_client = boto3.client("s3")
sqs_resource = boto3.resource('sqs')
sqs_client = boto3.client('sqs')


def fetch_csv(bucket, filename):
    """
    Fetch the CSV from the S3 bucket, and return the data
    :param bucket: The Amazon S3 bucket
    :param filename: The filename of the CSV
    :return: CSV data as dict
    """
    data_object = s3_client.get_object(Bucket=bucket, Key=filename)
    parsed_result = {}
    for row in csv.DictReader(codecs.getreader('UTF-8')(data_object['Body'])):
        if row['Country'] not in parsed_result:
            parsed_result[row['Country']] = [row['UUID']]
        else:
            parsed_result[row['Country']].append(row['UUID'])

    return parsed_result

def send_sqs_msg(message, queue_url):
    response = sqs_client.send_message(QueueUrl=queue_url,
                                       MessageAttributes={
                                           'UUIDs': {
                                               'DataType': 'String',
                                               'StringValue': 'UUIDs of countries'
                                           }
                                       },
                                       MessageBody=message)

    return response['MessageId']


if __name__ == '__main__':
    print('Fetching CSV data...')
    csv_data = fetch_csv('stevegilissentestbucket', 'testdata_uuid.csv')
    print('Posting to SQS queue...')
    print(send_sqs_msg(json.dumps(csv_data), 'SteveGilissenTestQueue'))

