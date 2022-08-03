"""
s3-test.py
Testing AWS S3 bucket connectivity in Python
"""
import boto3
from botocore.exceptions import ClientError
import pprint
import pandas as pd

# Define global S3 client
s3_resource = boto3.resource('s3')
s3_client = boto3.client("s3")


def print_csv_files(bucket):
    """
    Prints all CSV files in the S3 bucket to the console
    :param bucket: The bucket name
    :return:
    """
    _bucket = s3_resource.Bucket(bucket)
    # Quick list comprehension to get the key for each file in the bucket
    _keys = [object_summary.key for object_summary in _bucket.objects.all()]

    # Let's open each file in the bucket, check if it's a CSV by extension and make a nice printout of each row.
    for file in _keys:
        print(f'\nFile: {file} \n================')
        if file[-4:] == '.csv':
            data = s3_client.get_object(Bucket=bucket, Key=file)
            # Create a Pandas dataframe from the CSV file. This way, the printout is slightly neater.
            df = pd.read_csv(data['Body'])
            print(df)
        else:
            pprint.pprint('!! File is not a CSV file.')


if __name__ == '__main__':
    print_csv_files('stevegilissentestbucket')
