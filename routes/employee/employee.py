from fastapi import APIRouter
from starlette.responses import JSONResponse

from db.database_utils import initiate_query
from src.functions.auth_utils import get_user
from src.models.employee import Employee

employee_router = APIRouter()


@employee_router.get('/leaderboard')
def leaderboard():
	"""

	:return:
	"""
	
	leaderboard_details = initiate_query("select emp.name, emp.score from employee")
	
	if not leaderboard_details or isinstance(leaderboard_details['data'], dict):
		leaderboard_list = list() if not leaderboard_details else [leaderboard_details]
		return JSONResponse({"success": True, "course_details": leaderboard_list}, status_code=200)
	
	return JSONResponse({"success": True, "course_details": leaderboard_details['data']}, status_code=200)


@employee_router.get('/{emp}')
def get_employee_details(emp):
	"""

	:return:
	"""
	
	employee_details = get_user(username=emp, email=emp)
	
	if not employee_details:
		return JSONResponse({"success": False, "message": "incorrect employee code"}, status_code=404)
	
	return JSONResponse({"success": True, "employee_details": employee_details.__dict__}, status_code=200)


@employee_router.put('/details')
def update_employee_details(employee_details: Employee):
	"""
	
	:return:
	"""
	
	print(employee_details.__dict__)

	update = initiate_query(
		f"""update employee set name='{employee_details.name}', email_id='{employee_details.email_id}', skills='{employee_details.skills}', qualifications='{employee_details.qualifications}' where employee.username='{employee_details.username}'""")
	
	if update['success']:
		return JSONResponse({"success": True, "message": "updated successfully"}, status_code=200)
	else:
		return JSONResponse({"success": False, "message": "internal server error"}, status_code=500)
