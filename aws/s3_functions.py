from aws.boto_objects import s3Client
from config.settings import current_config


def put_to_s3(key, payload):
	"""
	
	:param key:
	:param payload:
	:return:
	"""
	
	s3Client.put_object(Body=payload, Bucket=current_config.AWS_S3_BUCKET, Key=key)


def get_presigned_url(key):
	return s3Client.generate_presigned_url(
		ClientMethod='get_object',
		Params={
			'Bucket': current_config.AWS_S3_BUCKET,
			'Key': key
		}
	)


def get_s3_file_object(key: str):
	"""
	
	:param key:
	:return:
	"""
	
	try:
		return s3Client.get_object(Bucket=current_config.AWS_S3_BUCKET, Key=key)['Body'].read()
	except Exception as e:
		print(f'Error getting file from S3 >> {e}')
		return dict()


def upload_file_to_s3(file):
	path = 'courses/' + file.filename
	# print(file.content_type)
	print(file.file.read())
	# s3Resource.Object(current_config.AWS_S3_BUCKET, path).put(Body=file.file.read(), ContentType=file.content_type)
	
	return path
