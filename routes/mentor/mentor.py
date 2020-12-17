import json

from fastapi import APIRouter
from starlette.responses import JSONResponse

from config.settings import current_config
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
	
	mentor_details = get_user(username=mentor, email=mentor, mode=current_config.MODES[1])
	
	if not mentor_details:
		return JSONResponse({"success": False, "message": "incorrect employee code"}, status_code=404)
	
	mentor_details = mentor_details.__dict__
	
	courses = initiate_query(f"call get_courses_from_mentor('{mentor}')")
	if not courses or isinstance(courses['data'], dict):

		course_list = list() if not courses else [json.loads(json.dumps(courses['data'], cls=DatetimeEncoder))]

		mentor_details['courses'] = course_list
	else:
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
		f"update mentor set name={mentor_details.name}, email_id={mentor_details.email_id}"
		f"where mentor.username={mentor_details.username}")
	
	if update['success']:
		return JSONResponse({"success": True, "message": "updated successfully"}, status_code=200)
	else:
		return JSONResponse({"success": False, "message": "internal server error"}, status_code=500)


@mentor_router.get('/{mentor_id}/courses')
def get_courses_by_mentor(mentor_id: int):
	"""
	Get all courses created by the mentor
	
	:param mentor_id:
	:return:
	"""
	
	db_details = initiate_query(f"call get_course_details_by_mentor_id('{mentor_id}')")
	
	if not db_details['data'].get('course_id'):
		return JSONResponse({"success": False, "message": "no course details found"}, status_code=404)
	
	return JSONResponse({"success": True, "course_details": db_details['data']}, status_code=200)
