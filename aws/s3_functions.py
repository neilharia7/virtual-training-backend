from aws.boto_objects import s3Client, s3Resource
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


def upload_file_to_s3(file_path: str, file_data, content_type):
	"""
	
	:param file_path:
	:param file_data:
	:param content_type:
	:return:
	"""
	path = 'courses/' + file_path.split('/')[-1]  # get the filename
	
	s3Resource.Object(current_config.AWS_S3_BUCKET, path).put(Body=file_data, ContentType=content_type)
	return path


def upload_audio_s3(retrieve_file_path: str, link_path: str):
	"""
	
	:param retrieve_file_path:
	:param link_path:
	:return:
	"""
	
	s3Client.upload_file(retrieve_file_path, current_config.AWS_S3_BUCKET, link_path)
