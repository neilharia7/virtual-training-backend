from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import Response, JSONResponse

from config.settings import current_config
from db.database_utils import initiate_query
from src.functions.auth_utils import authenticate_user, get_user, create_token, pwd_context
from src.models.register import Register

auth_router = APIRouter()
security = HTTPBasic()


@auth_router.post('/register/{mode}')
async def register(mode, details: Register):
	"""
	
	:return:
	"""
	
	# check if username alredy exists
	user_details = dict()
	
	if mode == current_config.MODES[0]:
		user_details = get_user(details.username, details.email)
	
	elif mode == current_config.MODES[1]:
		user_details = get_user(details.username, details.email, mode)
	
	query_mode = "insert_employee_details" if mode == current_config.MODES[0] else "insert_mentor_details"
	
	if mode not in current_config.MODES:
		return JSONResponse({"success": False, "message": "Invalid mode"}, status_code=406)
	
	if user_details:
		return JSONResponse({"success": False, "message": "username or email id already exists"}, status_code=406)
	
	else:
		password = pwd_context.hash(details.password)
		initiate_query(
			f"call {query_mode}('{details.name}', '{details.username}', '{password}', '{details.email}')")
		
		return JSONResponse({"success": True, "message": "registered successfully"}, status_code=200)


@auth_router.post("/login")
def login(request: Request, auth: HTTPBasicCredentials = Depends(security, use_cache=True)):
	"""
	
	:param request:
	:param auth:
	:return:
	"""
	
	user_login_mode = "mentor"
	
	if not auth:
		response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
		return response
	
	try:
		
		username, password = auth.username, auth.password
		print(f'username {username}\npassword {password}')
		print(request.client)
		user = authenticate_user(username, password, current_config.MODES[1])
		
		if not user:
			user = authenticate_user(username, password, current_config.MODES[0])
			user_login_mode = "employee"
			if not user:
				raise HTTPException(status_code=400, detail="Incorrect email or password")
		
		user_details = user.__dict__
		user_details['success'] = True
		user_details['access_mode'] = user_login_mode
		user_details['id'] = user_details.get('mentor_id') if user_details.get('mentor_id') else user_details.get('employee_id')
		
		response = JSONResponse(user_details, status_code=200)
		response.set_cookie(
			"Authorization",
			value=f"Bearer {create_token(username=username)}",
			# domain="uat.algo360.com",
			httponly=False,
			max_age=current_config.ACCESS_TOKEN_EXPIRE_MINUTES,
			expires=current_config.ACCESS_TOKEN_EXPIRE_MINUTES,
		)
		return response
	
	except HTTPException as e:
		print(f"error > {e.detail}")
		response = JSONResponse({"success": False, "message": e.detail}, status_code=401)
		return response


@auth_router.post("/logout")
async def route_logout_and_remove_cookie():
	"""

	:return:
	"""
	response = JSONResponse({"success": True}, status_code=200)
	response.delete_cookie("Authorization")
	return response
