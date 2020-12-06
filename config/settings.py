import os

HOST = os.getenv('APP_HOST', '0.0.0.0')
PORT = os.getenv('APP_PORT', 8800)
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
	"""Parent configuration class"""
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET = os.getenv('SECRET', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
	ALGORITHM = os.getenv('ALGORITHM', 'HS256')
	ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_MINUTES', 43200)  # 30 days
	API_DOCS_URL = True  # url => <domair>/docs/
	ALLOW_ORIGIN = ['*']
	DATABASE_SERVER = "testserver.crhcifgoezvo.ap-south-1.rds.amazonaws.com"
	DATABASE_NAME = "training_db"
	USERNAME = "vtp_training"
	PASSWORD = "15272b0ba39b474b8baeb7177f3e26bd"
	MODES = ["employee", "mentor"]
	
	AWS_S3_REGION = "ap-south-1"
	AWS_S3_BUCKET = "digitalfi"


class DevConfig(Config):
	"""Development configurations."""
	DEBUG = True


class TestConfig(Config):
	DEBUG = True
	TESTING = True


class StagConfig(Config):
	"""Staging or UAT configurations."""
	DEBUG = True


class ProdConfig(Config):
	"""Production configurations."""
	DEBUG = False
	
	# Setting the variable to false disables the docs in production
	API_DOCS_URL = False  # default True for all other environments


application_config = {
	"development": DevConfig,
	"testing": TestConfig,
	"staging": StagConfig,
	"production": ProdConfig
}

# Testing
current_config = application_config.get('development')
