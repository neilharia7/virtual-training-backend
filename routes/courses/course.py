import json
import os
import shutil
from threading import Thread

from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse

from aws.s3_functions import upload_file_to_s3
from db.database_utils import initiate_query
from src.functions.course_builder import build_scorm_compatible_course
from src.functions.utils import DatetimeEncoder
from src.models.assignment import AssignmentStatus
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
def upload_course(assignment_name: str, course_id: int, assignment_description: str, assignment_credits: int,
                  duration_hrs: int, file: UploadFile = File(...)):
	"""
	
	:param assignment_name:
	:param course_id:
	:param assignment_description:
	:param assignment_credits:
	:param duration_hrs:
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
		f"""call insert_assignment_details('{assignment_name}', '{course_id}', '{assignment_description}', '{assignment_credits}', '{duration_hrs}')""")
	
	assignment_details = initiate_query(f"""call get_assignment_details('{assignment_name}', 0)""")
	assignment_id = assignment_details['data'].get("assignment_id")
	
	_ = Thread(
		target=build_scorm_compatible_course,
		args=(assignment_id, file.filename, assignment_description)).start()
	
	return JSONResponse({
		"success": True, "file_name": file.filename, "assignment_name": assignment_name,
		"assignment_id": assignment_id}, status_code=200)


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
	
	assignment_details = initiate_query(
		f"call get_assignment_details('', {data.assignment_id})")
	
	if assignment_details['data']:
		return JSONResponse(
			{"Success": True, "status": assignment_details['data'].get('upload_status')},
			status_code=200)
	
	else:
		return JSONResponse({"success": False, "message": "assignment id not found"}, status_code=404)


@course_router.get('/audio/details/{audio_id}')
def get_audio_details(audio_id):
	"""
	
	:param audio_id:
	:return:
	"""
	
	try:
		
		with open(f'{os.getcwd()}/course_data/{audio_id}_audio.txt', 'r') as af:
			data = af.read()
		
		return JSONResponse({"success": True, "audio_details": data}, status_code=200)
	except Exception as e:
		print(f"error >> {e}")
		
		return JSONResponse({"success": False, "message": "audio file not found"}, status_code=404)
