from pydantic import BaseModel


class Assignment(BaseModel):
	assignment_name: str
	course_id: int
	assignment_description: str
	assignment_credits: int
	duration_hrs: int


class AssignmentStatus(BaseModel):
	assignment_id: int
