from pydantic import BaseModel


class Course(BaseModel):
	mentor_id: int
	course_name: str
	course_description: str
	duration: float
	credits: int
	prerequisites: list
	course_level: str
