from fastapi import APIRouter
from pydantic import BaseModel

import os

heartbeat = APIRouter()
from starlette.responses import JSONResponse


class Health(BaseModel):
	success: bool = True


@heartbeat.get("/", response_model=Health)
@heartbeat.post("/", response_model=Health)
def health_check():
	"""
	
	:return: json string
	"""
	print(os.getcwd())
	os.system(f'ruby {os.getcwd()}/ppt_to_scorm_compliant.rb Neil Haria')

	return JSONResponse({"success": True}, status_code=200)
