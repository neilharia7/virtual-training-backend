import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import current_config, HOST, PORT


def create_app():
	"""
	
	:return:
	"""
	app = FastAPI(
		title="Virtual Training Platform",
		description="""Industry focused courses where employees can track their progress,
		have Q&A sessions with mentors and improve their skill-set. Mentors can track individual’s performance,
		overall ranking and use the same to recommend respective project managers in the organization"""
	)
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
	from routes.courses.course import course_router
	from routes.scorm.scorm_conversion import convert_router
	
	app.include_router(auth_router, tags=['Authenticate'], prefix='/auth')
	app.include_router(course_router, tags=['Course'], prefix='/courses')
	app.include_router(heartbeat, tags=['Health'])
	app.include_router(convert_router, tags=['Scorm'], prefix='/scorm')
	return app


application = create_app()

if __name__ == "__main__":
	uvicorn.run(application, host=HOST, port=PORT)
