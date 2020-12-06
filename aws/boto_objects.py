import boto3

from config.settings import current_config

region_name = current_config.AWS_S3_REGION

s3Resource = boto3.resource('s3', region_name=region_name)
s3Client = boto3.client('s3', region_name=region_name)
