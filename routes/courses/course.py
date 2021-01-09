import json
import os
import shutil

from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse

from aws.s3_functions import upload_file_to_s3
from db.database_utils import initiate_query
from src.functions.utils import DatetimeEncoder
from src.models.assignment import Assignment, AssignmentStatus
from src.models.course import Course

course_router = APIRouter()


def course_details(course_id: int = None):
	"""
	
	:param course_id:
	:return:
	"""
	
	if course_id:
		courses = initiate_query(f"call get_course_details('{course_id}')")
	else:
		courses = initiate_query("call get_courses()")
	
	if not courses or isinstance(courses['data'], dict):
		course_list = list() if not courses else [json.loads(json.dumps(courses['data'], cls=DatetimeEncoder))]
		return JSONResponse({"success": True, "course_details": course_list}, status_code=200)
	
	return JSONResponse(
		json.loads(json.dumps({"success": True, "course_details": courses['data']}, cls=DatetimeEncoder)),
		status_code=200)


@course_router.get('/{course_id}')
def get_course_details(course_id):
	"""
	
	:return:
	"""
	try:
		course_id = int(course_id)
		return course_details(course_id=course_id)
	except ValueError as e:
		print(f'error >> {e}')
		return JSONResponse({"success": False, "message": "invalid mentor id"}, status_code=400)


@course_router.get('/')
def get_courses():
	"""
	
	:return:
	"""
	
	return course_details()


@course_router.post('/assignment/upload')
def upload_course(data: Assignment, file: UploadFile = File(...)):
	"""
	
	:param data:
	:param file:
	:return:
	"""
	print(f'filename {file.filename}')
	
	file_path = f"{os.getcwd()}/course_data/{file.filename}"
	content_type = file.content_type
	
	with open(file_path, 'wb') as buffer:
		shutil.copyfileobj(file.file, buffer)
	
	with open(file_path, 'rb') as file_data:
		upload_file_to_s3(file_path, file_data.read(), content_type)
	
	initiate_query(
		f"call insert_assignment_details('{data.assignment_name}', '{data.course_id}', '{data.assignment_description}', '{data.assignment_credits}', '{data.duration_hrs}')")
	
	assignment_details = initiate_query(f"call get_assignment_details('{data.assignment_name}', 0")
	
	asisgnment_id = assignment_details['data'].get("assignment_id")
	
	return {
		"success": True, "file_name": file.filename, "assignment_name": data.assignment_name,
		"assignment_id": asisgnment_id}


@course_router.put('/details')
def insert_course_details(data: Course):
	"""
	
	:param data:
	:return:
	"""
	
	initiate_query(
		f"call insert_course_details('{data.course_name}', '{data.course_description}', '{data.course_level}', {data.mentor_id}, '{data.duration}', {data.credits}, '{data.prerequisites}')")
	
	return {"success": True}


@course_router.get('/assignment/upload/status')
def assignment_upload_status(data: AssignmentStatus):
	"""
	
	:return:
	"""
	
	assignment_details = initiate_query(f"call get_assignment_details('', {data.assignment_id})")
	
	if assignment_details['data']:
		return JSONResponse(
			{"Success": True, "status": assignment_details['data'].get('upload_status')},
			status_code=200)
	
	else:
		return JSONResponse({"success": False, "message": "assignment id not found"}, status_code=404)
