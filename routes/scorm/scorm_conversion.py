import os

from fastapi import APIRouter
from fastapi.security import HTTPBasic

security = HTTPBasic()
convert_router = APIRouter()


@convert_router.post('/ppt-to-images')
def convert_ppt_to_images():
	"""
	
	:return:
	"""
	
	# hardcoded for now
	os.system(f'libreoffice --headless --convert-to pdf {os.getcwd()}/course_data/Clustering.pptx')
	
	os.system(f'convert -density 400 -resize 3000^ {os.getcwd()}/course_data/cluster%d.jpg')
	
	return {"success": True}


@convert_router.post('/images-to-scorm')
def convert_images_to_scorm():
	"""
	
	:return:
	"""
	
	os.system(f'ruby {os.getcwd()}/ppt_to_scorm_compliant.rb')
	
	return {"success": True}
