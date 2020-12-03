from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from config.settings import current_config
from db.database_utils import initiate_query
from src.models.db import EmployeeInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
	"""
	checks whether the hash of `plain_password` matches with the `hashed_password
	
	:param plain_password:
	:param hashed_password:
	:return: boolean value
	"""
	return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
	"""
	
	:param username:
	:return:
	"""
	
	response = initiate_query(f"call get_details_from_username_or_email('{username}')")
	
	if response['success']:
		user_details = response['data']
		return EmployeeInDB(**user_details)


def authenticate_user(username: str, password: str):
	"""
	
	:param username:
	:param password:
	:return:
	"""
	
	user = get_user(username)
	if not user:
		return False
	if not verify_password(password, user.password):
		return False
	
	return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
	"""
	
	:param data:
	:param expires_delta:
	:return:
	"""
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, current_config.SECRET, algorithm=current_config.ALGORITHM)
	return encoded_jwt
