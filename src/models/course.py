from pydantic import BaseModel


class Course(BaseModel):
	course_name: str
	course_description: str
	duration: str
	credits: int
	prerequisites: list
