from pydantic import BaseModel


class Employee(BaseModel):
	employee_name: str
	username: str
	email_id: str = None
	skills: str = None
	qualifications: str = None
	score: str = None
	certificates: str = None
	active_status: bool = None
