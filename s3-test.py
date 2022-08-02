"""
s3-test.py
Testing AWS S3 bucket connectivity in Python
"""
import boto3
from botocore.exceptions import ClientError

# Define global S3 client
s3 = boto3.resource('s3')


def get_files(bucket):
    """
    List all files stored in the bucket
    :param bucket: The bucket name
    :return:
    """
    _bucket = s3.Bucket(bucket)
    for object_summary in _bucket.objects.all():
        print(object_summary)


if __name__ == '__main__':
    get_files('stevegilissentestbucket')
