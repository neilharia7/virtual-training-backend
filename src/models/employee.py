from pydantic import BaseModel


class Employee(BaseModel):
	name: str
	username: str
	email_id: str = None
	skills: list = None
	qualifications: list = None
	score: str = None
	certificates: list = None
	# active_status: bool = None
	
	#  if the user is present in the database
	success: bool = True
