import json

from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse

from aws.s3_functions import upload_file_to_s3
from db.database_utils import initiate_query
from src.functions.utils import DatetimeEncoder

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

@course_router.post('/upload')
def upload_course(file: UploadFile = File(...)):
	"""
	
	:return:
	"""
	
	print(f'filename {file.filename}')
	upload_file_to_s3(file)
	
	return {"success": True}
# =======
	
# 	with open(f'{os.getcwd()}/.{file.filename.split(".")[-1]}', 'wb') as buffer:
# 		shutil.copyfileobj(file.file, buffer)
	
# 	return {"success": True}
# >>>>>>> Stashed changes
