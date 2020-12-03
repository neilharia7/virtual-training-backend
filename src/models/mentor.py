from pydantic import BaseModel


class Mentor(BaseModel):
	mentor_name: str
	username: str
	email_id: str = None
	active_status: bool = None
	
	#  if the user is present in the database
	success: bool = True
