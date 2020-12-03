from src.models.employee import Employee
from src.models.mentor import Mentor


class EmployeeInDB(Employee):
	password: str


class MentorInDB(Mentor):
	password: str
