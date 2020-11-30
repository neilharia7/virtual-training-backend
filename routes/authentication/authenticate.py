import base64
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import Response, JSONResponse

from config.settings import current_config
from src.data.information import fake_users_db
from src.functions.auth_utils import authenticate_user
from src.functions.auth_utils import create_access_token
from src.security.auth import basic_auth, BasicAuth

auth_router = APIRouter()


@auth_router.post("/login")
async def login(auth: BasicAuth = Depends(basic_auth)):
	if not auth:
		response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
		return response
	
	try:
		decoded = base64.b64decode(auth).decode("ascii")
		username, _, password = decoded.partition(":")
		user = authenticate_user(fake_users_db, username, password)
		if not user:
			raise HTTPException(status_code=400, detail="Incorrect email or password")
		
		access_token_expires = timedelta(minutes=current_config.ACCESS_TOKEN_EXPIRE_MINUTES)
		access_token = create_access_token(
			data={"sub": username}, expires_delta=access_token_expires
		)
		
		token = jsonable_encoder(access_token)
		
		response = JSONResponse({"status": "success"}, status_code=200)
		response.set_cookie(
			"Authorization",
			value=f"Bearer {token}",
			# domain="localtest.me",
			httponly=True,
			max_age=current_config.ACCESS_TOKEN_EXPIRE_MINUTES,
			expires=current_config.ACCESS_TOKEN_EXPIRE_MINUTES,
		)
		return response
	
	except HTTPException as e:
		print(f"error > {e.detail}")
		response = JSONResponse({"status": "error", "message": e.detail}, status_code=401)
		return response


@auth_router.post("/logout")
async def route_logout_and_remove_cookie():
	"""

	:return:
	"""
	response = JSONResponse({"status": "success"}, status_code=200)
	response.delete_cookie("Authorization")
	return response
