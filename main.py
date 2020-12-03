import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import current_config, PORT


def create_app():
	"""
	
	:return:
	"""
	app = FastAPI()
	app.add_middleware(
		CORSMiddleware,
		allow_origins=current_config.ALLOW_ORIGIN,
		allow_credentials=True,
		allow_methods=['*'],
		allow_headers=['*']
	)
	
	app.debug = current_config.DEBUG
	
	from routes.authentication.authenticate import auth_router
	from routes.heartbeat import heartbeat
	
	app.include_router(auth_router, tags=['Authenticate'], prefix='/auth')
	app.include_router(heartbeat, tags=['Health'])
	
	return app


application = create_app()

if __name__ == "__main__":
	uvicorn.run(application, port=PORT)
