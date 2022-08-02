"""
sqs-test.py
Testing AWS SQS connectivity in Python
"""
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# Define global S3 client
sqs_resource = boto3.resource('sqs')
sqs_client = boto3.client('sqs')


def list_queues():
    """
    List all queues available
    :return:
    """
    try:
        sqs_queues = []
        for queue in sqs_resource.queues.all():
            sqs_queues.append(queue)
    except ClientError as e:
        print(f'Could not list queues. {e.response["Error"]["Message"]}')
    else:
        return sqs_queues


def send_test_message(message, queue_url):
    response = sqs_client.send_message(QueueUrl=queue_url,
                                       MessageAttributes={
                                           'Title': {
                                               'DataType': 'String',
                                               'StringValue': 'Test Message'
                                           }
                                       },
                                       MessageBody=message)
    return response['MessageId']


def receive_next_message(queue_url, delete=False):
    response = sqs_client.receive_message(QueueUrl=queue_url,
                                          AttributeNames=[
                                              'SentTimestamp'
                                          ],
                                          MaxNumberOfMessages=1,
                                          MessageAttributeNames=[
                                              'All'
                                          ])
    message = response['Messages'][0]
    print(message)
    receipt_handle = message['ReceiptHandle']

    if delete:
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        print(f'Deleted message with handle {receipt_handle}')

    return f'MessageID: {message["MessageId"]} - Message: {message["Body"]}'


def get_queue_url(queue):
    response = sqs_client.get_queue_url(QueueName=queue)
    return response['QueueUrl']


if __name__ == '__main__':
    # get_queue_url('SteveGilissenTestQueue')
    current_datetime = datetime.now().isoformat()
    queue_name = get_queue_url('SteveGilissenTestQueue')
    print('Sending test message...')
    print('Result: ' + send_test_message(f'New test sent on {current_datetime}', queue_name))
    print('Retrieve message...')
    print('Result: ' + receive_next_message(queue_name, True))
