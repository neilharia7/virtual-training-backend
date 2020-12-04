from datetime import datetime, timedelta

import jwt
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

from config.settings import current_config
from db.database_utils import initiate_query
from src.models.db import EmployeeInDB, MentorInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
	"""
	checks whether the hash of `plain_password` matches with the `hashed_password`
	
	:param plain_password:
	:param hashed_password:
	:return: boolean value
	"""
	return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str, email: str = '', mode: str = current_config.MODES[0]):
	"""
	
	:param username:
	:param email:
	:param mode:
	:return:
	"""
	print(username, email, mode)
	if mode == current_config.MODES[0]:
		response = initiate_query(f"call get_emp_details_from_username_or_email('{username}', '{email}')")
		
		if response['data']:
			return EmployeeInDB(**response['data'])
	else:
		response = initiate_query(f"call get_mentor_details_from_username_or_email('{username}', '{email}')")
		
		if response['data']:
			return MentorInDB(**response['data'])


def authenticate_user(username: str, password: str, mode: str = current_config.MODES[0]):
	"""
	
	:param username:
	:param password:
	:param mode:
	:return:
	"""
	
	# authentication can be by username or by email
	user = get_user(username=username, email=username, mode=mode)
	if not user:
		return False
	if not verify_password(plain_password=password, hashed_password=user.password):
		return False
	
	# removing `password` as it need not be sent in the response
	user.__dict__.pop('password')
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


def create_token(username: str):
	"""
	
	:param username:
	:return:
	"""
	
	access_token_expires = timedelta(minutes=current_config.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": username}, expires_delta=access_token_expires
	)
	
	return jsonable_encoder(access_token)
