from fastapi import APIRouter
from pydantic import BaseModel

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
	return JSONResponse({"success": True}, status_code=200)
