import json

from fastapi import APIRouter
from starlette.responses import JSONResponse

from db.database_utils import initiate_query
from src.functions.auth_utils import get_user
from src.functions.utils import DatetimeEncoder
from src.models.mentor import Mentor

mentor_router = APIRouter()


@mentor_router.get('/{mentor}')
def get_mentor_details(mentor):
	"""

	:return:
	"""
	
	mentor_details = get_user(username=mentor, email=mentor)
	
	if not mentor_details:
		return JSONResponse({"success": False, "message": "incorrect employee code"}, status_code=404)
	
	mentor_details = mentor_details.__dict__
	
	courses = initiate_query("call get_courses_by_mentor()")
	if not courses or isinstance(courses['data'], dict):
		course_list = list() if not courses else [json.loads(json.dumps(courses['data'], cls=DatetimeEncoder))]
		mentor_details['courses'] = course_list
	
	mentor_details['courses'] = courses['data']
	
	return JSONResponse(
		json.loads(json.dumps({"success": True, "mentor_details": mentor_details}, cls=DatetimeEncoder)),
		status_code=200)


@mentor_router.put('/details')
def update_mentor_details(mentor_details: Mentor):
	"""
	
	:return:
	"""
	
	update = initiate_query(
		f"update mentor set mentor_name={mentor_details.name}, email_id={mentor_details.email_id}"
		f"where mentor.username={mentor_details.username}")
	
	if update['success']:
		return JSONResponse({"success": True, "message": "updated successfully"}, status_code=200)
	else:
		return JSONResponse({"success": False, "message": "internal server error"}, status_code=500)
