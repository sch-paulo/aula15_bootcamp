import boto3
from botocore.exceptions import NoCredentialsError
import sys
import os

class S3Client:
    def __init__(self):
        self._envs = {
            'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'region_name': os.environ.get('AWS_REGION', 'us-west-1'),
            's3_bucket': os.environ.get('S3_BUCKET_NAME'),
            'datalake': os.environ.get('DELTA_LAKE_S3_PATH')
        }

        for var in self._envs:
            if self._envs[var] is None:
                print(f'The environment variable {var} is not defined')
                sys.exit(1)

        self.s3 = boto3.client(
            's3', 
            aws_access_key_id=self._envs['aws_acces_key_id'], 
            aws_secret_access_key=self._envs['aws_secret_access_key'],
            region_name=self._envs['region_name']
            )

    def upload_file(self, data, s3_key):
        try:
            self.s3.put_object(Body=data.get_value(), Bucket=self._envs['s3_bucket'], Key=s3_key)
        except NoCredentialsError:
            print('Credentials not found. Make sure to set up your AWS credentials correctly.')

    def download_file(self, s3_key):
        try:
            file = self.s3.get_object(Bucket=self._envs['s3_bucket'], Key=s3_key)
            print(f'Successfull download for {s3_key}')
            return file
        except NoCredentialsError:
            print('Credentials not found. Make sure to set up your AWS credentials correctly.')
        except FileNotFoundError:
            print(f'File {s3_key} not found in bucket {self._envs['s3_bucket']}.')
        except Exception as e:
            print(f'An error occurred during download: {e}')

    def list_object(self, prefix):
        return self.s3.list_objects(Bucket=self._envs['s3_bucket'], Prefix=prefix)['Contents']
