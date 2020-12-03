from pydantic import BaseModel


class Register(BaseModel):
	username: str
	password: str
	name: str
	email: str
