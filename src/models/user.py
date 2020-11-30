from pydantic import BaseModel


class User(BaseModel):
	username: str
	email: str = None
	full_name: str = None
	disabled: bool = None
