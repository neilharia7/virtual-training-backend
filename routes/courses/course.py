import json

from fastapi import APIRouter
from starlette.responses import JSONResponse

from db.database_utils import initiate_query
from src.functions.utils import DatetimeEncoder

course_router = APIRouter()


def course_details(mentor_id: int = None):
	"""
	
	:param mentor_id:
	:return:
	"""
	
	if mentor_id:
		courses = initiate_query(f"call get_courses_from_mentor('{mentor_id}')")
	else:
		courses = initiate_query("call get_courses()")
	
	if not courses or isinstance(courses['data'], dict):
		course_list = list() if not courses else [json.loads(json.dumps(courses['data'], cls=DatetimeEncoder))]
		return JSONResponse({"success": True, "course_details": course_list}, status_code=200)
	
	return JSONResponse(
		json.loads(json.dumps({"success": True, "course_details": courses['data']}, cls=DatetimeEncoder)),
		status_code=200)


@course_router.get('/{mentor_id}')
def get_courses_by_mentor(mentor_id):
	"""
	
	:return:
	"""
	try:
		mentor_id = int(mentor_id)
		return course_details(mentor_id=mentor_id)
	except ValueError as e:
		print(f'error >> {e}')
		return JSONResponse({"success": False, "message": "invalid mentor id"}, status_code=400)


@course_router.get('/')
def get_courses():
	"""
	
	:return:
	"""
	
	return course_details()
