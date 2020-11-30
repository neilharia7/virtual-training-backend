import uvicorn
from fastapi import FastAPI

from config.settings import current_config, PORT


def create_app():
	"""
	
	:return:
	"""
	app = FastAPI()
	app.debug = current_config.DEBUG
	
	from routes.authentication.authenticate import auth_router
	from routes.heartbeat import heartbeat
	
	app.include_router(auth_router, prefix='/auth')
	app.include_router(heartbeat)
	
	return app


application = create_app()

if __name__ == "__main__":
	uvicorn.run(application, port=PORT)
