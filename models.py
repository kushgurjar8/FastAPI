from pydantic import BaseModel


class student(BaseModel):
    id: int
    name: str
    password: str

class Login(BaseModel):
    username: str
    password: str