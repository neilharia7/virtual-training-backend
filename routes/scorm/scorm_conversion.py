import os

from fastapi import APIRouter
from fastapi.security import HTTPBasic
from pydantic import BaseModel

security = HTTPBasic()
convert_router = APIRouter()


class CourseDetails(BaseModel):
	course_name: str
	description: str
	file_name: str


@convert_router.post('/ppt-to-images/{course_name}')
def convert_ppt_to_images(course_name: str):
	"""
	
	:return:
	"""
	print(f'libreoffice --headless --convert-to pdf {os.getcwd()}/course_data/{course_name}')
	os.system(f'libreoffice --headless --convert-to pdf {os.getcwd()}/course_data/{course_name}')
	
	print(
		f'convert -density 400 -resize 3000^ {os.getcwd()}/course_data/{course_name} {os.getcwd()}/course_data/{course_name.split(".")[0]}%d.jpg')
	os.system(
		f'convert -density 400 -resize 3000^ {os.getcwd()}/course_data/{course_name} {os.getcwd()}/course_data/{course_name.split(".")[0]}%d.jpg')
	
	return {"success": True}


@convert_router.post('/images-to-scorm')
def convert_images_to_scorm(data: CourseDetails):
	"""
	
	:return:
	"""
	
	os.system(f'ruby {os.getcwd()}/ppt_to_scorm_compliant.rb {data.course_name} {data.description} {data.file_name}')
	
	current_path = os.listdir(f'{os.getcwd()}/course_data')
	for item in current_path:
		if item.endswith('.jpg'):
			os.remove(os.path.join(current_path, item))
	
	return {"success": True}
