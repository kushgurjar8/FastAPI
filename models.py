from pydantic import BaseModel

from typing import Literal


# ----------------------------model for login with username----------------------
# class student(BaseModel):
#     id: int
#     name: str
#     password: str

# class Login(BaseModel):
#     username: str
#     password: str

# --------------------------------model for login with email-----------------------

class student(BaseModel):
    id: int
    name: str
    email: str    
    password: str

class Login(BaseModel):
    email: str           
    password: str


# --------------------------------model for RBAC--------------------------------------  


class employee(BaseModel):
    id: int
    name: str
    email: str
    password: str
    phone: str
    role: Literal["admin", "manager", "mentor", "employee"]
    branch: str

class EmpLogin(BaseModel):
    email: str
    password: str