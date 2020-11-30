from fastapi import APIRouter

heartbeat = APIRouter()
from starlette.responses import JSONResponse


@heartbeat.get("/")
async def heart_beat():
	"""
	
	:return:
	"""
	return JSONResponse({"status": "ok"}, status_code=200)
