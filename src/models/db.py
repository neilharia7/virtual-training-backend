from src.models.employee import Employee
from src.models.mentor import Mentor


class EmployeeInDB(Employee):
	password: str
	employee_id: int
	

class MentorInDB(Mentor):
	password: str
	mentor_id: int
