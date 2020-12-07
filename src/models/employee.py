from pydantic import BaseModel


class Employee(BaseModel):
	name: str
	username: str
	email_id: str = None
	skills: str = None
	qualifications: str = None
	score: str = None
	certificates: str = None
	about_me: str = None
	# active_status: bool = None
	
	#  if the user is present in the database
	success: bool = True
